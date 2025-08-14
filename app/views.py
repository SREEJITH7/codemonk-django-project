from django.shortcuts import render

# Create your views here.
from collections import Counter, defaultdict

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Paragraph, ParagraphWordFrequency, WordFrequency
from .serializers import RegisterSerializer, ParagraphIngestSerializer, SearchQuerySerializer
from .services.tokenize import tokenize, split_paragraphs


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class ParagraphIngestView(APIView):
    """
    POST /paragraphs
    body: { "content": "para1\\n\\npara2\\n\\n..." }
    """
    def post(self, request):
        serializer = ParagraphIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data["content"]
        user = request.user

        paras = split_paragraphs(content)

        created_ids = []
        per_para_counts = []  # list[Counter]

        with transaction.atomic():
            start_index = (
                Paragraph.objects.filter(user=user).order_by("-index").values_list("index", flat=True).first() or 0
            )
            # create Paragraphs keeping order
            new_paras = []
            for i, text in enumerate(paras, start=1):
                new_paras.append(Paragraph(user=user, index=start_index + i, text=text))
            Paragraph.objects.bulk_create(new_paras)

            # fetch created with IDs
            created = list(Paragraph.objects.filter(user=user, index__gt=start_index).order_by("index"))
            created_ids = [p.id for p in created]

            # per-paragraph counting
            for p in created:
                counts = Counter(tokenize(p.text))
                per_para_counts.append(counts)

            # bulk ParagraphWordFrequency
            pwf_objects = []
            for p, counts in zip(created, per_para_counts):
                for w, c in counts.items():
                    pwf_objects.append(
                        ParagraphWordFrequency(paragraph=p, word=w, count=c)
                    )
            ParagraphWordFrequency.objects.bulk_create(pwf_objects, ignore_conflicts=True)

            # upsert WordFrequency totals
            # aggregate per-user word totals from this batch
            user_totals = defaultdict(int)
            for counts in per_para_counts:
                for w, c in counts.items():
                    user_totals[w] += c

            # try update existing rows
            existing = WordFrequency.objects.filter(user=user, word__in=user_totals.keys())
            existing_map = {wf.word: wf for wf in existing}
            to_update = []
            to_create = []
            for w, c in user_totals.items():
                if w in existing_map:
                    wf = existing_map[w]
                    wf.total_count = wf.total_count + c
                    to_update.append(wf)
                else:
                    to_create.append(WordFrequency(user=user, word=w, total_count=c))

            if to_create:
                WordFrequency.objects.bulk_create(to_create)
            if to_update:
                WordFrequency.objects.bulk_update(to_update, ["total_count"])

        return Response({"paragraph_ids": created_ids, "count": len(created_ids)}, status=status.HTTP_201_CREATED)


class SearchView(APIView):
    """
    GET /search?word=hello&limit=10
    """
    def get(self, request):
        q = SearchQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        word = q.validated_data["word"].strip().lower()
        # normalize like tokenizer: strip leading/trailing punctuation
        from .services.tokenize import PUNCT_STRIP_RE
        word = PUNCT_STRIP_RE.sub("", word)
        limit = q.validated_data["limit"]

        if not word:
            return Response({"detail": "word is required after normalization."}, status=400)

        qs = (
            ParagraphWordFrequency.objects
            .filter(paragraph__user=request.user, word=word)
            .select_related("paragraph")
            .order_by("-count", "paragraph__index")
        )[:limit]

        results = []
        for item in qs:
            p = item.paragraph
            # optional: simple excerpt using first occurrence
            text = p.text
            tokens = tokenize(text)
            try:
                first_idx = tokens.index(word)
                # build a small excerpt around the token index (approximate)
                excerpt = " ".join(tokens[max(0, first_idx-5): first_idx+6])
            except ValueError:
                excerpt = text[:120]
            results.append({
                "paragraph_id": p.id,
                "index": p.index,
                "count": item.count,
                "excerpt": excerpt,
            })

        return Response({"word": word, "results": results}, status=200)

from __future__ import annotations

import random
import textwrap
from dataclasses import dataclass
from typing import List


@dataclass
class CandidateEssay:
    topic_id: str
    topic: str
    candidate_id: int
    strategy: str
    essay: str


def _clean(text: str) -> str:
    return " ".join(textwrap.dedent(text).strip().split())


def _topic_terms(topic: str) -> str:
    words = [w.strip(".,!?;:()[]{}\"'") for w in topic.split()]
    words = [w for w in words if len(w) > 4]
    return ", ".join(words[:5]) if words else topic


def generate_template_candidates(topic_id: str, topic: str, n_candidates: int = 6, seed: int = 42) -> List[CandidateEssay]:
    """Generate several essay styles for one topic.

    This is intentionally original student code, not a direct copy of any Kaggle kernel.
    The goal is not prompt injection. The goal is to create candidate essays whose quality
    depends on the judge's preference: strict academic, creative, concise, skeptical, etc.
    """
    rnd = random.Random(seed + int(abs(hash(str(topic_id))) % 10_000))
    key_terms = _topic_terms(topic)

    templates = []

    templates.append((
        "baseline_academic",
        f"""
        The question of {topic} requires a balanced answer rather than a simple yes or no.
        A strong position should consider benefits, risks, and the conditions under which the
        idea works best. In my view, the most reasonable conclusion is that the topic has real
        value, but only when it is guided by clear responsibility and human judgement.

        First, the positive side is that {key_terms} can create opportunities for learning,
        efficiency, and wider participation. When people use the idea carefully, it can reduce
        barriers and help individuals make better decisions. This is especially important in
        modern society, where information changes quickly and people need flexible tools.

        However, the same idea can also create problems if it is used without critical thinking.
        Overconfidence, unfair access, and weak evaluation can lead to poor outcomes. For that
        reason, people should not treat the idea as a perfect solution. It should support human
        reasoning, not replace it.

        Therefore, the best answer is moderation. The topic is useful when it improves fairness,
        understanding, and practical outcomes, but it becomes harmful when people ignore its
        limits. A responsible approach should combine innovation with ethics, evidence, and
        continuous review.
        """,
    ))

    templates.append((
        "creative_reflective",
        f"""
        {topic} is not only a technical or social question; it is a mirror of how people decide
        what progress should mean. Every new idea promises speed, convenience, and possibility,
        but it also asks us what we are willing to lose in exchange.

        On one side, the idea can open doors. It can help people who previously lacked access,
        give learners new ways to explore, and allow communities to solve problems faster. In
        this sense, {key_terms} can be a bridge between limitation and opportunity.

        On the other side, a bridge can also be crossed too quickly. If people accept every new
        solution without asking who benefits, who is left behind, and what values are being
        weakened, progress becomes shallow. A good society should not only ask whether something
        works. It should also ask whether it works fairly and wisely.

        For this reason, I support the idea with caution. It should be used as a tool for better
        judgement, not as an excuse to stop thinking. The real challenge is not choosing between
        acceptance and rejection, but learning how to use change without being controlled by it.
        """,
    ))

    templates.append((
        "concise_direct",
        f"""
        I partly agree with the statement about {topic}. The idea can be useful because it may
        improve access, save time, and help people solve problems more effectively. It can also
        encourage new forms of learning and communication.

        Even so, it should not be accepted blindly. Any system involving {key_terms} can create
        unfairness, dependency, or low-quality decisions if users do not check its limitations.
        The result depends on how the idea is designed, who controls it, and whether people are
        trained to use it responsibly.

        Overall, the best position is balanced. The idea is beneficial when it supports human
        judgement and social fairness. It is risky when it replaces careful thinking. Therefore,
        it should be adopted with clear rules, regular evaluation, and awareness of its limits.
        """,
    ))

    templates.append((
        "skeptical_logic",
        f"""
        A careful discussion of {topic} should begin with a warning: popularity is not the same
        as quality. Many people accept new ideas because they sound modern, but a convincing
        argument must be based on outcomes, not excitement.

        The strongest argument in favour is practical. The idea may improve speed, access, and
        consistency. It may help people organise information and make decisions with less effort.
        These benefits matter, especially when resources are limited.

        Still, the weaknesses are serious. If the system is poorly designed, it may reward surface
        appearance more than real understanding. If access is unequal, it may increase existing
        gaps. If users become passive, it may reduce independent judgement. These risks are not
        imaginary; they follow from relying too heavily on any tool without accountability.

        My conclusion is cautious support. The idea should be used only when its benefits can be
        measured and its harms can be reduced. A responsible policy would include transparency,
        human review, and a willingness to stop using the approach when it fails.
        """,
    ))

    templates.append((
        "pro_contrast",
        f"""
        There are two reasonable ways to view {topic}. The optimistic view is that the idea makes
        life more efficient and inclusive. It can help people reach information faster, organise
        work better, and participate in situations that were previously difficult for them.

        The critical view is that efficiency alone is not enough. A society can become faster while
        becoming less thoughtful. When decisions are shaped by convenience, people may ignore
        deeper questions about fairness, responsibility, and long-term effects. This is especially
        relevant to {key_terms}, because the result depends strongly on context.

        I believe the optimistic view is stronger, but only under strict conditions. The idea should
        be introduced gradually, explained clearly, and reviewed regularly. People should be taught
        not only how to use it, but also when to doubt it.

        In conclusion, the issue is not whether the idea is good or bad in itself. It is good when
        it strengthens human ability and bad when it weakens human responsibility. The correct
        answer is careful adoption, not blind acceptance.
        """,
    ))

    templates.append((
        "structured_headings",
        f"""
        Introduction. The topic, {topic}, should be evaluated through usefulness, fairness, and
        long-term impact. These three criteria give a clearer answer than personal opinion alone.

        Usefulness. The idea can be useful because it may reduce time, improve access, and support
        better organisation. In many real situations, people need tools that help them handle
        complex information. This gives the idea practical value.

        Fairness. The main concern is unequal benefit. If only some groups understand or access
        the system, the result may increase inequality. A fair approach must include guidance,
        transparent rules, and support for people who are disadvantaged.

        Long-term impact. The idea should not make people passive. It should strengthen critical
        thinking and decision-making. If it reduces responsibility, then its convenience becomes a
        weakness.

        Conclusion. I support the idea only as a controlled and evaluated tool. Its value depends
        on responsible use, not on the technology or concept alone.
        """,
    ))

    # More diversity when n_candidates is large.
    templates.append((
        "empathetic_social",
        f"""
        Discussions about {topic} often focus on systems and results, but the human experience is
        just as important. A policy or tool can be technically impressive and still fail if people
        feel confused, excluded, or pressured by it.

        The advantage is that the idea may help ordinary users. It can make tasks easier, support
        people with fewer resources, and offer new ways to participate. When designed with care,
        it can make society more open and responsive.

        The danger is that people may be judged by a system they do not understand. They may also
        become dependent on a process that appears objective but still reflects human assumptions.
        This is why transparency and education are essential.

        My final view is that the idea should be accepted, but not treated as neutral or perfect.
        It must be shaped around human dignity, fairness, and accountability. Progress should make
        people more capable, not less heard.
        """,
    ))

    templates.append((
        "uncertainty_aware",
        f"""
        It is tempting to give a confident answer to {topic}, but the truth is conditional. The
        answer changes depending on who uses the idea, how it is implemented, and what safeguards
        exist.

        In a strong implementation, the idea can support better choices. It can improve speed,
        access, and consistency. It can also reduce repetitive work and allow people to focus on
        more meaningful tasks. These are real advantages.

        In a weak implementation, the same idea can create dependency, hidden bias, and superficial
        judgement. Users may trust the result too quickly simply because it appears organised or
        official. That would be a serious mistake.

        For this reason, my answer is cautious and evidence-based. The idea should be tested,
        compared with alternatives, and improved through feedback. It should be judged by actual
        outcomes rather than promises. Used responsibly, it can help; used carelessly, it can harm.
        """,
    ))

    rnd.shuffle(templates)
    selected = templates[: max(1, n_candidates)]
    return [
        CandidateEssay(
            topic_id=str(topic_id),
            topic=topic,
            candidate_id=i,
            strategy=strategy,
            essay=_clean(text),
        )
        for i, (strategy, text) in enumerate(selected)
    ]

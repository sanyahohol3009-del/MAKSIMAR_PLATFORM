from __future__ import annotations

from tools.jarvis_live_runtime.memory_context_builder import JarvisBrainContext
from tools.jarvis_live_runtime.memory_context_sources import _asks_style_memory_recall
from tools.jarvis_live_runtime.voice_response_cleaner import contains_forbidden_generic_tail

def _answer_conversation_style_complaint_if_grounded(context: JarvisBrainContext) -> str:
    lowered = context.user_text.casefold()
    if _looks_like_keyboard_layout_noise(context.user_text):
        return (
            "Похоже, раскладка поехала. Я не буду лепить заготовку вместо смысла: "
            "повтори фразу нормальной раскладкой, и я разберу её по делу."
        )
    if _asks_template_style_complaint(lowered):
        return (
            "Да, брат, вижу петлю: я начал повторять canned-ответ вместо реакции на смысл. "
            "Это не нормальный разговор. Чинить надо в двух местах: fast-chat guard не должен пропускать "
            "заготовки, а session memory не должна кормить их обратно в следующий ответ. "
            "Для обычного общения держу живой стиль: прямо, по делу, но не сухим шаблоном."
        )
    if _asks_casual_state_question(lowered):
        return (
            "На связи, брат. По состоянию честно: чат работает, но я вижу риск шаблонной петли, "
            "поэтому обычный разговор надо держать живым guard'ом и памятью последних реплик, "
            "а не одной дежурной фразой."
        )
    return ""


def _asks_template_style_complaint(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "шаблон",
            "заготов",
            "одно и то же",
            "один и тот же ответ",
            "перестань шаблон",
            "почему ты мне шаблон",
            "отвечаешь шаблон",
            "не живой",
            "живее",
        )
    )


def _asks_casual_state_question(lowered: str) -> bool:
    cleaned = lowered.strip(" ?!.,")
    return cleaned in {"как дела", "как ты", "ты как", "как состояние", "ты на связи"}


def _looks_like_keyboard_layout_noise(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 10:
        return False
    letters = [char for char in stripped if char.isalpha()]
    if not letters:
        return False
    latin_letters = [char for char in letters if "a" <= char.casefold() <= "z"]
    cyrillic_letters = [char for char in letters if "а" <= char.casefold() <= "я" or char.casefold() == "ё"]
    punctuation_noise = sum(1 for char in stripped if char in "&;,./[]{}")
    return len(latin_letters) >= max(8, len(letters) * 3 // 4) and not cyrillic_letters and punctuation_noise > 0


def _is_forbidden_chat_template_response(response_text: str) -> bool:
    return contains_forbidden_generic_tail(response_text)


def _repair_forbidden_chat_template_response(context: JarvisBrainContext) -> str:
    if _asks_template_style_complaint(context.user_text.casefold()):
        return _answer_conversation_style_complaint_if_grounded(context)
    return (
        "Сбил шаблонный ответ и не сохраняю его как нормальную память. "
        "По смыслу текущего запроса отвечаю заново: мне нужно держаться фактов из контекста, "
        "а если фактов не хватает — прямо сказать, что нужна проверка."
    )


def _answer_style_memory_recall_if_grounded(context: JarvisBrainContext) -> str:
    lowered = context.user_text.casefold()
    if not _asks_style_memory_recall(lowered):
        return ""
    profile = context.stable_style_profile
    relation = str(profile.get("relation_style", "")).strip()
    communication = str(profile.get("communication_style", "")).strip()
    avoid = str(profile.get("avoid", "")).strip()
    concise_rule = str(profile.get("concise_rule", "")).strip()
    stored_style = " ".join((relation, communication, avoid, concise_rule, context.rolling_summary, *context.local_chat_memory_snippets)).casefold()
    if not any(marker in stored_style for marker in ("брат", "напарник", "гараж", "not template-like", "шаблон")):
        return ""
    return (
        "Да, брат, помню. Ты хочешь, чтобы я был не сухим помощником, "
        "а JARVIS-напарником по гаражу: говорил прямо, живо, по делу, "
        "не слишком коротко и без шаблонных концовок с дежурным предложением помощи. "
        "Буду держать этот стиль в следующих сессиях."
    )


def _asks_weather_or_current_facts(lowered: str) -> bool:
    return any(marker in lowered for marker in ("погода", "курс", "новости", "сейчас в интернете", "поиск"))


def _asks_pc_action(lowered: str) -> bool:
    return any(marker in lowered for marker in ("открой", "запусти", "клик", "напечатай", "управляй", "выключи пк"))


def _asks_permanent_memory_write(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "запиши это в постоянную память",
            "сохрани в постоянную память",
            "canonical memory",
            "global memory",
            "запомни навсегда",
        )
    )

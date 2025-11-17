from collections.abc import Generator, Sequence
from .tokenize import Token, TokenType, tokenize

def parse(rule: str) -> 'RuleNode':
    tokens = list(tokenize(rule))
    rule_node, remaining_tokens = _rule_node(tokens)
    if remaining_tokens:
        raise ValueError(f"Unexpected tokens remaining after parsing: {remaining_tokens}")
    return rule_node

def _pop_if_token_type(tokens: Sequence[Token], token_type: TokenType) -> tuple[Token | None, Sequence[Token]]:
    if tokens and tokens[0].type == token_type:
        return tokens[0], tokens[1:]
    return None, tokens

def _require_token_type(tokens: Sequence[Token], token_type: TokenType, context: str | None = None) -> tuple[Token, Sequence[Token]]:
    if tokens and tokens[0].type == token_type:
        return tokens[0], tokens[1:]
    raise ValueError(f"Required token of type {token_type}, but got {tokens[0].type if tokens else 'EOF'}" + (f" in {context}" if context else ""))


type RuleSyntaxNode = \
    PrefixedRuleSyntaxNode | \
    PostfixRuleSyntaxNode

type PrefixedRuleSyntaxNode = \
    WordNode | \
    OptionalNode | \
    GroupNode | \
    ListNode | \
    CaptureNode

type PostfixRuleSyntaxNode = \
    ZeroOrMoreNode | \
    OneOrMoreNode | \
    ChoiceNode

INDENT_SIZE = 2

def _rule_syntax_node(tokens: Sequence[Token]) -> tuple[RuleSyntaxNode | None, Sequence[Token]]:
    prefixed_node, tokens = _rule_syntax_node_prefixed(tokens)
    if not prefixed_node:
        return None, tokens
    postfixed_node, tokens = _rule_syntax_node_postfixed(prefixed_node, tokens)
    if postfixed_node:
        return postfixed_node, tokens
    return prefixed_node, tokens

def _rule_syntax_node_prefixed(tokens: Sequence[Token]) -> tuple[PrefixedRuleSyntaxNode | None, Sequence[Token]]:
    # Prefixed
    optional_node, tokens = _optional_node(tokens)
    if optional_node:
        return optional_node, tokens

    group_node, tokens = _group_node(tokens)
    if group_node:
        return group_node, tokens

    list_node, tokens = _list_node(tokens)
    if list_node:
        return list_node, tokens

    capture_node, tokens = _capture_node(tokens)
    if capture_node:
        return capture_node, tokens

    words_node, tokens = _words_node(tokens)
    if words_node:
        return words_node, tokens

    return None, tokens

def _rule_syntax_node_postfixed(previous: RuleSyntaxNode, tokens: Sequence[Token]) -> tuple[RuleSyntaxNode | None, Sequence[Token]]:
    # Postfixed
    zero_or_more_node, tokens = _zero_or_more_node(previous, tokens)
    if zero_or_more_node:
        return zero_or_more_node, tokens

    one_or_more_node, tokens = _one_or_more_node(previous, tokens)
    if one_or_more_node:
        return one_or_more_node, tokens

    choice_node, tokens = _choice_node(previous, tokens)
    if choice_node:
        return choice_node, tokens

    return None, tokens


class WordNode:
    def __init__(self, words_token: Token):
        self.words_token = words_token

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}WordNode(word={self.words_token.value})"

def _words_node(tokens: Sequence[Token]) -> tuple[WordNode | None, Sequence[Token]]:
    words_token, tokens = _pop_if_token_type(tokens, TokenType.WORDS)
    if words_token:
        return WordNode(words_token), tokens
    return None, tokens

class OptionalNode:
    def __init__(self, children: list[RuleSyntaxNode]):
        self.children = children

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}OptionalNode:"
        for child in self.children:
            yield from child.lines(spaces + INDENT_SIZE)

def _optional_node(tokens: Sequence[Token]) -> tuple[OptionalNode | None, Sequence[Token]]:
    optional_start, tokens = _pop_if_token_type(tokens, TokenType.OPTIONAL_START)
    if not optional_start:
        return None, tokens

    children: list[RuleSyntaxNode] = []
    while tokens and tokens[0].type != TokenType.OPTIONAL_END:
        child, tokens = _rule_syntax_node(tokens)
        if child:
            children.append(child)
        else:
            break

    _, tokens = _require_token_type(tokens, TokenType.OPTIONAL_END, "optional segment")
    return OptionalNode(children), tokens

class ZeroOrMoreNode:
    def __init__(self, child: RuleSyntaxNode):
        self.child = child

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}ZeroOrMoreNode:"
        yield from self.child.lines(spaces + INDENT_SIZE) 

def _zero_or_more_node(previous: RuleSyntaxNode, tokens: Sequence[Token]) -> tuple[ZeroOrMoreNode | None, Sequence[Token]]:
    zero_or_more, tokens = _pop_if_token_type(tokens, TokenType.ZERO_OR_MORE)
    if not zero_or_more:
        return None, tokens

    return ZeroOrMoreNode(previous), tokens

class OneOrMoreNode:
    def __init__(self, child: RuleSyntaxNode):
        self.child = child

    def __str__(self) -> str:
        return "\n".join(self.lines(0))
    
    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}OneOrMoreNode:"
        yield from self.child.lines(spaces + INDENT_SIZE)

def _one_or_more_node(previous: RuleSyntaxNode, tokens: Sequence[Token]) -> tuple[OneOrMoreNode | None, Sequence[Token]]:
    one_or_more, tokens = _pop_if_token_type(tokens, TokenType.ONE_OR_MORE)
    if not one_or_more:
        return None, tokens

    return OneOrMoreNode(previous), tokens

class ChoiceNode:
    def __init__(self, left: RuleSyntaxNode, right: RuleSyntaxNode):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}ChoiceNode:"
        yield f"{' ' * (spaces + INDENT_SIZE)}Left:"
        yield from self.left.lines(spaces + 2 * INDENT_SIZE)
        yield f"{' ' * (spaces + INDENT_SIZE)}Right:"
        yield from self.right.lines(spaces + 2 * INDENT_SIZE)

def _choice_node(left: RuleSyntaxNode, tokens: Sequence[Token]) -> tuple[ChoiceNode | None, Sequence[Token]]:
    choice, tokens = _pop_if_token_type(tokens, TokenType.CHOICE)
    if not choice:
        return None, tokens

    right, tokens = _rule_syntax_node(tokens)
    if not right:
        raise ValueError("Expected right node after choice operator")

    return ChoiceNode(left, right), tokens

class GroupNode:
    def __init__(self, children: list[RuleSyntaxNode]):
        self.children = children

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}GroupNode:"
        for child in self.children:
            yield from child.lines(spaces + INDENT_SIZE)

def _group_node(tokens: Sequence[Token]) -> tuple[GroupNode | None, Sequence[Token]]:
    group_start, tokens = _pop_if_token_type(tokens, TokenType.GROUP_START)
    if not group_start:
        return None, tokens

    children: list[RuleSyntaxNode] = []
    while tokens and tokens[0].type != TokenType.GROUP_END:
        child, tokens = _rule_syntax_node(tokens)
        if child:
            children.append(child)
        else:
            break

    _, tokens = _require_token_type(tokens, TokenType.GROUP_END, "group segment")
    return GroupNode(children), tokens

class ListNode:
    def __init__(self, reference: Token):
        self.reference = reference

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}ListNode(reference={self.reference.value})"

def _list_node(tokens: Sequence[Token]) -> tuple[ListNode | None, Sequence[Token]]:
    list_start, tokens = _pop_if_token_type(tokens, TokenType.LIST_START)
    if not list_start:
        return None, tokens

    reference_token, tokens = _require_token_type(tokens, TokenType.WORDS)
    _, tokens = _require_token_type(tokens, TokenType.LIST_END, "list segment")

    return ListNode(reference_token), tokens

class CaptureNode:
    def __init__(self, reference: Token):
        self.reference = reference

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}CaptureNode(reference={self.reference.value})"

def _capture_node(tokens: Sequence[Token]) -> tuple[CaptureNode | None, Sequence[Token]]:
    capture_start, tokens = _pop_if_token_type(tokens, TokenType.CAPTURE_START)
    if not capture_start:
        return None, tokens

    reference_token, tokens = _require_token_type(tokens, TokenType.WORDS)
    _, tokens = _require_token_type(tokens, TokenType.CAPTURE_END, "capture segment")

    return CaptureNode(reference_token), tokens

class RuleNode:
    def __init__(self, children: list[RuleSyntaxNode], start_anchored: bool, end_anchored: bool):
        self.children = children
        self.start_anchored = start_anchored
        self.end_anchored = end_anchored

    def __str__(self) -> str:
        return "\n".join(self.lines(0))

    def lines(self, spaces: int) -> Generator[str]:
        yield f"{' ' * spaces}RuleNode(start_anchored={self.start_anchored}, end_anchored={self.end_anchored}):"
        for child in self.children:
            yield from child.lines(spaces + INDENT_SIZE)

def _rule_node(tokens: Sequence[Token]) -> tuple[RuleNode, Sequence[Token]]:
    start_anchor, tokens = _pop_if_token_type(tokens, TokenType.START_ANCHOR)
    children: list[RuleSyntaxNode] = []
    child: RuleSyntaxNode | None = None
    while tokens:
        child, tokens = _rule_syntax_node(tokens)
        if child:
            children.append(child)
        else:
            break

    end_anchor, tokens = _pop_if_token_type(tokens, TokenType.END_ANCHOR)
    return RuleNode(children, start_anchored=start_anchor is not None, end_anchored=end_anchor is not None), tokens
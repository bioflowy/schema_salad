from typing import Any, Callable, ClassVar, Generic, List, Optional, Set, TypeVar, Union

from typing_extensions import Literal, NotRequired, Required, TypeAlias, TypedDict

AstType = Literal[
    "text",
    "image",
    "codespan",
    "linebreak",
    "inline_html",
    "heading",
    "newline",
    "thematic_break",
    "block_code",
    "block_html",
    "list",
    "list_item",
]
_AstChildren: TypeAlias = "AstChildren"
AstObject = TypedDict(
    "AstObject",
    {
        "type": Required[AstType],
        "text": Required[Optional[_AstChildren]],
        "link": NotRequired[str],
        "info": NotRequired[Optional[str]],
        "children": NotRequired[Union[_AstChildren, List[_AstChildren]]],
        "ordered": NotRequired[bool],
        "level": NotRequired[int],
    },
    total=False,
)
AstChildren = Union[AstObject, str]

HTMLType = str
DataT = TypeVar("DataT", bound=Union[AstChildren, HTMLType])

RenderMethod = Union[
    Callable[[], DataT],  # blank
    Callable[[DataT, Any], DataT],
]

class BaseRenderer(Generic[DataT]):
    NAME: ClassVar[str] = "base"

    def _get_method(self, name: AstType) -> RenderMethod[DataT]: ...
    def finalize(self, data: DataT) -> Any: ...

class AstRenderer(BaseRenderer[AstChildren]):
    NAME: ClassVar[Literal["ast"]] = "ast"

    def __init__(
        self, escape: bool = True, allow_harmful_protocols: Optional[bool] = None
    ) -> None: ...
    def _create_default_method(self, name: AstType) -> RenderMethod[AstChildren]: ...
    def _get_method(self, name: AstType) -> RenderMethod[AstChildren]: ...
    def text(self, text: str) -> AstChildren: ...
    def link(
        self, link: str, text: Optional[str] = None, title: Optional[str] = None
    ) -> AstChildren: ...
    def image(
        self, src: str, alt: str = "", title: Optional[str] = None
    ) -> AstChildren: ...
    def codespan(self, text: str) -> AstChildren: ...
    def linebreak(self, text: str) -> AstChildren: ...
    def inline_html(self, text: str) -> AstChildren: ...
    def paragraph(self, text: str) -> AstChildren: ...
    def heading(self, text: str, level: int) -> AstChildren: ...
    def newline(self) -> AstChildren: ...
    def thematic_break(self) -> AstChildren: ...
    def block_code(self, code: str, info: Optional[str] = None) -> AstChildren: ...
    def block_html(self, html: str) -> AstChildren: ...
    def list(
        self, children: str, ordered: bool, level: int, start: Optional[int] = None
    ) -> AstChildren: ...
    def list_item(self, children: str, level: int) -> AstChildren: ...
    def finalize(self, data: DataT) -> List[DataT]: ...

class HTMLRenderer(BaseRenderer[HTMLType]):
    NAME: ClassVar[Literal["html"]] = "html"
    HARMFUL_PROTOCOLS: ClassVar[Set[str]]
    _escape: bool
    _allow_harmful_protocols: Optional[bool]

    def __init__(
        self, escape: bool = True, allow_harmful_protocols: Optional[bool] = None
    ) -> None: ...
    def _safe_url(self, url: str) -> str: ...
    def text(self, text: str) -> HTMLType: ...
    def link(
        self, link: str, text: Optional[str] = None, title: Optional[str] = None
    ) -> HTMLType: ...
    def image(
        self, src: str, alt: str = "", title: Optional[str] = None
    ) -> HTMLType: ...
    def emphasis(self, text: str) -> HTMLType: ...
    def strong(self, text: str) -> HTMLType: ...
    def codespan(self, text: str) -> HTMLType: ...
    def linebreak(self, text: str) -> HTMLType: ...
    def inline_html(self, text: str) -> HTMLType: ...
    def paragraph(self, text: str) -> HTMLType: ...
    def heading(self, text: str, level: int) -> HTMLType: ...
    def newline(self) -> HTMLType: ...
    def thematic_break(self) -> HTMLType: ...
    def block_code(self, code: str, info: Optional[str] = None) -> HTMLType: ...
    def block_quote(self, text: str) -> HTMLType: ...
    def block_html(self, html: str) -> HTMLType: ...
    def block_error(self, html: str) -> HTMLType: ...
    def list(
        self, text: str, ordered: bool, level: int, start: Optional[int] = None
    ) -> HTMLType: ...
    def list_item(self, text: str, level: int) -> HTMLType: ...
    def finalize(self, data: DataT) -> HTMLType: ...
from typing import Any, Dict, Optional


class imdict(dict):
    """Immutable dictionary."""

    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError("This object is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class Result(imdict):
    """
    An immutable Result object representing
    both Success and Error results from functions and APIs.
    """

    def __init__(
        self,
        success: bool,
        message: str = "",
        instance: Any = None,
        errors: Optional[Dict] = None,
        tag: Optional[str] = None,
        error_code: Optional[str] = None,
    ):
        self.is_success = success
        self.message = message
        self.instance = instance
        self.tag = tag
        if not self.tag:
            self.tag = "success" if success else "error"
        self.is_error = True if self.tag == "error" else False
        self.is_warning = True if self.tag == "warning" else False
        self.errors = errors
        self.error_code = error_code
        dict.__init__(self, is_success=success, message=message, errors=errors)

    @classmethod
    def success(cls, message="", instance=None):
        return cls(True, message, instance=instance)

    @classmethod
    def warning(cls, message="", instance=None, error_code=""):
        return cls(
            False, message, instance=instance, error_code=error_code, tag="warning"
        )

    @classmethod
    def error(cls, message="", instance=None, errors=None, error_code=""):
        return cls(
            False, message, instance=instance, errors=errors, error_code=error_code
        )

    @classmethod
    def from_dict(cls, source: Dict):
        if (
            "result" not in source
            or "message" not in source
            or source.get("class_name", "") != "lava_core.utils.Result"
        ):
            raise TypeError("Invalid source dict.")

        tag = source["result"]
        is_success = True if tag == "success" else False

        return cls(
            success=is_success,
            message=source["message"],
            instance=source.get("instance", None),
            errors=source.get("errors", None),
            error_code=source.get("error_code", None),
            tag=tag,
        )

    def to_dict(self):
        result = "success" if self.is_success else "error"
        if self.is_warning:
            result = "warning"

        res_dict = {
            "class_name": "lava.utils.Result",
            "result": result,
            "message": str(self.message),
        }

        if not self.is_success:
            res_dict["errors"] = self.errors or []
            res_dict["error_code"] = self.error_code
        if self.instance:
            res_dict["object"] = self.instance

        return res_dict

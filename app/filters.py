from .models import now


def format_datetime(value, code='%A, %B %-m, %Y %H:%M:%S') -> str:
    """Format datetimes in jinja templates."""
    return value.strftime(code) if value else ''


def format_float(value, default='', digits=None) -> str:
    """Format floats in jinja templates."""
    try:
        if digits is None:
            return f"{float(value):g}"
        else:
            return f"{float(value):.{digits}f}"
    except (ValueError, TypeError):
        return default


def register_filters(app):
    """Register custom jinja template filters."""
    # Custom jinja template functions
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['float'] = format_float
    app.jinja_env.globals['now'] = now

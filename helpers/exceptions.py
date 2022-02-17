# CR: [MD] I recommend having an app-global base exception class to always differ between builting exceptions and app-level exceptions
# I.E. `SportipyExceptionBase`
# And have custom-defined exceptions inherit it. That way you can `except` only your exceptions (as `except`ing an `Except` is bad)
# CR: [MD] It's good practice to have custom exception classes to end with 'Error' or 'Exception' in their name.
class PlaylistNameAlreadyExists(Exception):
    pass


class ReachedFreePlaylistsLimit(Exception):
    pass


class ReachedFreePlaylistSongsLimit(Exception):
    pass

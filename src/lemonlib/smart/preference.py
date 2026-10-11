from wpilib import Preferences, RobotController

from typing import TypeVar, Generic

T = float | bool | int | str
PreferenceT = TypeVar("PreferenceT", bound=T)


class SmartPreference(Generic[PreferenceT]):
    """
    Wrapper for wpilib Preferences that allows for previous values from NetworkTables 
    to be remembered between sessions.
    """
    _low_bandwidth_mode = False
    _cache_period = 250_000

    def __init__(
        self, 
        key: str,
        default_value: PreferenceT, 
    ) -> None:
        """
        Initializes `SmartPreference`.
        
        Args:
            key: The key (directory) for the value (i.e. "some_value"). Will be saved under
                 the "Preferences/" directory in Networktables.
            default_value: The default value for the preference.
        """

        self._default_value = default_value
        self._key = key

        self._create_preference(default_value)
        self._last_value = self._read()
        self._last_nt_read = RobotController.getFPGATime()

    def _create_preference(self, default_value: PreferenceT) -> None:
        """
        Creates a preference instance for this object.
        """
        if isinstance(default_value, bool):
            Preferences.initBoolean(self._key, default_value)
        elif isinstance(default_value, float):
            Preferences.initDouble(self._key, default_value)
        elif isinstance(default_value, int):
            Preferences.initInt(self._key, default_value)
        else:
            Preferences.initString(self._key, default_value)

    def _read(self) -> PreferenceT:
        """
        Reads the underlying value in NetworkTables.
        """
        default = self._default_value
        if isinstance(default, bool):
            return Preferences.getBoolean(self._key, default)
        if isinstance(default, float):
            return Preferences.getDouble(self._key, default)
        if isinstance(default, int):
            return Preferences.getInt(self._key, default)
        return Preferences.getString(self._key, default)

    @staticmethod
    def set_cache_period(cache_period: int) -> None:
        """
        Sets the cache period for all `SmartPreference` instances between reads in NT.

        Args:
            cache_period: The period in microseconds.
        """
        SmartPreference._cache_period = cache_period

    @staticmethod
    def low_bandwidth_mode(enabled: bool) -> None:
        """
        Sets the state of low bandwidth mode for all `SmartPreference` instances.
        Low bandwidth mode means that only the default value that each instance was initialized
        with will be used rather than any other set value (programmatically or in NT).
        """
        SmartPreference._low_bandwidth_mode = enabled

    def set(self, value: PreferenceT) -> None:
        """
        Sets the value of the preference.
        """
        default = self._default_value
        if isinstance(default, bool):
            Preferences.setBoolean(self._key, bool(value))
        elif isinstance(default, float):
            Preferences.setDouble(self._key, float(value))
        elif isinstance(default, int):
            Preferences.setInt(self._key, int(value))
        else:
            Preferences.setString(self._key, str(value))

        self._last_value = value

    def get(self) -> PreferenceT:
        """
        Returns the underlying value of the preference.
        """
        if SmartPreference._low_bandwidth_mode:
            return self._default_value

        # Only re-read from NT periodically to avoid per-cycle overhead
        current_time = RobotController.getFPGATime()
        if current_time - self._last_nt_read < self._cache_period:
            return self._last_value

        self._last_nt_read = current_time

        new_value = self._read()
        self._last_value = new_value
        return new_value

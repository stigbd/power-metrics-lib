"""Athlete model."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import uuid4


@dataclass
class Athlete:
    """Athlete class.

    Attributes:
        name (str): The athlete's name.
        ftp (list[tuple[date, int]]): The athlete's FTPs ordered by date.
        weight (list[tuple[date, float]]): The athlete's weight ordered by date.
        uuid (str): The athlete's UUID.

    """

    name: str
    _ftp: list[tuple[date, int]] | None = None
    _weight: list[tuple[date, float]] | None = None
    uuid: str | None = str(uuid4())

    def __init__(
        self, name: str, ftp: int | None = None, weight: float | None = None
    ) -> None:
        """Initialize the athlete object."""
        self.name = name
        if ftp:
            self.set_ftp(ftp)
        if weight:
            self.set_weight(weight)

    def get_ftp(self, from_date: str | None = None) -> int | None:
        """Get the FTP for a specific date.

        If the from_date is not given, the latest FTP is returned.

        Args:
            from_date (str): The date ("yyyy-mm-dd") to get the FTP for.

        Returns:
            int: The FTP.
        """
        # If no ftp is set, return None:
        if self._ftp is None:
            return None
        # If no from_date is given, return the latest FTP:
        if from_date is None:
            return self._ftp[0][1] if self._ftp else None
        # Find the FTP for the given date:
        _from_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=UTC).date()
        for ftp in self._ftp:
            if ftp[0] <= _from_date:
                return ftp[1]

        return None

    def set_ftp(self, ftp: int, from_date: str | None = None) -> None:
        """Set the FTP for a specific date.

        If the from_date is not given, the FTP is set for today.

        Args:
            ftp (int): The FTP to set.
            from_date (str): The date ("yyyy-mm-dd") to set the FTP for.
        """
        if self._ftp is None:
            self._ftp = []

        # If no from_date is given, set the FTP for today:
        if from_date is None:
            _from_date = datetime.now(UTC).date()
        else:
            _from_date = (
                datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=UTC).date()
            )
        self._ftp.append((_from_date, ftp))
        # sort the list by date in descending order:
        self._ftp = sorted(self._ftp, key=lambda x: x[0], reverse=True)

    def get_all_ftps(self) -> list[tuple[str, int]] | None:
        """Get all FTPs and their dates.

        Returns:
            list[tuple[str, int]]: The FTPs and their dates.
        """
        if self._ftp is None:
            return None

        return [(ftp[0].strftime("%Y-%m-%d"), ftp[1]) for ftp in self._ftp]

    def set_weight(self, weight: float, from_date: str | None = None) -> None:
        """Set the weight for a specific date.

        If the from_date is not given, the weight is set for today.

        Args:
            weight (float): The weight (kg) to set.
            from_date (str): The date ("yyyy-mm-dd") to set the weight for

        """
        if self._weight is None:
            self._weight = []

        # If no from_date is given, set the FTP for today:
        if from_date is None:
            _from_date = datetime.now(UTC).date()
        else:
            _from_date = (
                datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=UTC).date()
            )
        self._weight.append((_from_date, weight))
        # sort the list by date in descending order:
        self._weight = sorted(self._weight, key=lambda x: x[0], reverse=True)

    def get_weight(self, from_date: str | None = None) -> float | None:
        """Get the weight for a specific date.

        If the from_date is not given, the latest weight is returned.

        Args:
            from_date (str): The date ("yyyy-mm-dd") to get the weight for.

        Returns:
            float: The weight.
        """
        # If no weight is set, return None:
        if self._weight is None:
            return None
        # If no from_date is given, return the latest weight:
        if from_date is None:
            return self._weight[0][1] if self._weight else None
        _from_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=UTC).date()

        # Find the weight for the given date:
        for weight in self._weight:
            if weight[0] <= _from_date:
                return weight[1]

        return None

    def get_all_weights(self) -> list[tuple[str, float]] | None:
        """Get all weights and their dates.

        Returns:
            list[tuple[str, float]]: The weights and their dates.
        """
        if self._weight is None:
            return None

        return [(weight[0].strftime("%Y-%m-%d"), weight[1]) for weight in self._weight]

    def get_ftp_pr_kg(self, from_date: str | None = None) -> float | None:
        """Get ftp per kg (w/kg) for a specific date.

        If the from_date is not given, the latest w/kg is returned.

        Args:
            from_date (str): The date ("yyyy-mm-dd") to get the w/kg for.

        Returns:
            float: The w/kg.
        """
        weight = self.get_weight(from_date)
        ftp = self.get_ftp(from_date)

        if weight is None or ftp is None:
            return None
        return weight / ftp

    def get_all_ftp_pr_kg(self) -> list[tuple[str, float]] | None:
        """Get all ftp per kg (w/kg) and their dates.

        Returns:
            list[tuple[str, float]]: The w/kg and their dates.
        """
        if self._weight is None or self._ftp is None:
            return None

        # Merge the ftps and weights and calculate the w/kg:
        ftp_pr_kg = []
        # Concatenate the dates from the ftps and weights:
        dates = set(
            [ftp[0] for ftp in self._ftp] + [weight[0] for weight in self._weight]
        )
        # Sort the dates in descending order:
        dates = sorted(dates, reverse=True)
        # Calculate the w/kg for each date:
        for _date in dates:
            ftp = self.get_ftp(_date.strftime("%Y-%m-%d"))
            weight = self.get_weight(_date.strftime("%Y-%m-%d"))
            if weight is not None and ftp is not None:  # pragma: no branch
                ftp_pr_kg.append((_date.strftime("%Y-%m-%d"), ftp / weight))

        return ftp_pr_kg

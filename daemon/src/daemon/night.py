from daemon.main import get_time_from_env, main
from daemon.utils import get_env_variable
from datetime import datetime, timedelta


if __name__ == "__main__":
    station_id = int(get_env_variable("STATION_ID"))
    start_time = get_time_from_env("NIGHT_START")
    end_time = get_time_from_env("NIGHT_END")
    date = datetime.today().date() - timedelta(days=1)
    main(station_id, start_time, end_time, date, True)

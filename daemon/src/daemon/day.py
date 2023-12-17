from daemon.main import get_time_from_env, main
from daemon.utils import get_env_variable
from datetime import datetime


if __name__ == "__main__":
    print("HELLO!")
    station_id = int(get_env_variable("STATION_ID"))
    start_time = get_time_from_env("DAY_START")
    end_time = get_time_from_env("DAY_END")
    date = datetime.today().date()
    main(station_id, start_time, end_time, date, True)

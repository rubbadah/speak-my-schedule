import datetime

import pytz


def format_schedule(date, schedule):
    """
    スケジュールをフォーマット

    Args:
        date (str): 日付（形式: YYYYMMDD）
        schedule (list): イベントのリスト（各イベントは辞書形式で、'startTime'と'title'を含む）

    Returns:
        str: フォーマットされたスケジュールの文字列
    """
    date_obj = datetime.datetime.strptime(date, "%Y%m%d")
    jst_timezone = pytz.timezone("Asia/Tokyo")
    date_obj = date_obj.astimezone(jst_timezone)
    date_str = f"{date_obj.month}月{date_obj.day}日"

    if not schedule:
        return f"{date_str}の予定はありません。"

    events_str = []
    for event in schedule:
        event_date = convert_to_jst(
            event["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if date_obj <= event_date:
            events_str.append(
                f"{event_date.hour}時{event_date.minute}分から{event['title']}"
            )

    events_list = "、".join(events_str)
    return f"{date_str}の予定は{len(events_str)}件です。{events_list}。"


def convert_to_jst(api_date_str, time_format):
    """
    日付文字列を日本標準時（JST）に変換

    Args:
        api_date_str (str): 日付文字列
        time_format (str): 日付文字列のフォーマット

    Returns:
        datetime: JSTに変換された日付オブジェクト
    """
    api_date = datetime.datetime.strptime(api_date_str, time_format)
    utc_timezone = pytz.timezone("UTC")
    api_date = utc_timezone.localize(api_date)
    jst_timezone = pytz.timezone("Asia/Tokyo")
    jst_date = api_date.astimezone(jst_timezone)
    return jst_date
    return jst_date

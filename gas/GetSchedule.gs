// Googleカレンダーから指定した日付の予定を取得
function doGet(e) {
  try {
    console.log("start Custom Actions GetSchedule");

    // リクエストからパラメータを取得
    console.log("e: " + JSON.stringify(e));
    var dateString = e.parameter.Day;
    // console.log("e.parameter.Day: " + e.parameter.Day);

    // 日付の文字列から年、月、日を取得
    var year = parseInt(dateString.substring(0, 4), 10);
    var month = parseInt(dateString.substring(4, 6), 10) - 1; // JavaScriptの月は0から始まる
    var day = parseInt(dateString.substring(6, 8), 10);

    // 指定された日付の始まりと終わりを示すDateオブジェクトを作成
    var startTime = new Date(year, month, day);
    var endTime = new Date(year, month, day + 1);

    // Googleカレンダーからイベントを取得
    var calendar = CalendarApp.getDefaultCalendar();
    var events = calendar.getEvents(startTime, endTime);

    // イベントの情報を含むオブジェクトの配列を作成
    var eventsData = events.map(function (event) {
      return {
        title: event.getTitle(),
        startTime: event.getStartTime().toISOString(), // ISO 8601形式の日付文字列
      };
    });

    // JSON形式で返す
    console.log("eventsData: " + eventsData);
    return ContentService.createTextOutput(
      JSON.stringify(eventsData)
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    // エラー発生時の処理
    console.error("Error adding event: " + error.message);
    return ContentService.createTextOutput("Error: " + error.message);
  }
}

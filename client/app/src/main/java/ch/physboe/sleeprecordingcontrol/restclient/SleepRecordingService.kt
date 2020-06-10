package ch.physboe.sleeprecordingcontrol.restclient

import ch.physboe.sleeprecordingcontrol.restclient.model.RecordingState
import com.android.volley.Request
import com.google.gson.Gson
import org.json.JSONObject

class SleepRecordingService {

    private val webService : SleepRecordingWebService = SleepRecordingWebService()
    private val gson : Gson = Gson()

    fun getRecordingState(completionHandler: (recordingState: RecordingState?) -> Unit) {
        webService.send(SleepRecordingWebService.RECORDING_SERVICE, null, Request.Method.GET) { response : JSONObject? ->
            val recordingState : RecordingState? = if (response != null) {
                gson.fromJson(response.toString(), RecordingState::class.java)
            } else {
                null
            }
            completionHandler(recordingState)

        }
    }

    fun putRecordingState(recordingState: RecordingState, completionHandler: () -> Unit) {
        val request = JSONObject(gson.toJson(recordingState))
        webService.send(SleepRecordingWebService.RECORDING_SERVICE, request, Request.Method.PUT) { response : JSONObject? ->
            completionHandler()

        }
    }

}
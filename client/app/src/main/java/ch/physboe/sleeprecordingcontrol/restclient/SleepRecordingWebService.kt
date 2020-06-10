package ch.physboe.sleeprecordingcontrol.restclient

import android.util.Log
import com.android.volley.AuthFailureError
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.VolleyLog
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject

class SleepRecordingWebService {
   companion object{
       val TAG = SleepRecordingWebService::class.java.simpleName
       val PING_SERVICE = "test"
       val REINSTALL_DB_SERVIE = "test/install"
       val RECORDING_SERVICE = "recording/"

   }

    private val basePath = "http://192.168.1.20:5000/api/"

    fun put(
        path: String,
        params: JSONObject?,
        completionHandler: (response: JSONObject?) -> Unit
    ) {


    }

    fun send(
        path: String,
        params: JSONObject?,
        method: Int,
        completionHandler: (response: JSONObject?) -> Unit
    ) {
        val jsonObjReq = object : JsonObjectRequest(method, basePath + path, params ,
            Response.Listener<JSONObject> { response ->
                Log.d(TAG, "/get request OK! Response: $response")
                completionHandler(response)
            },
            Response.ErrorListener { error ->
                VolleyLog.e(TAG, "/get request fail! Error: ${error.message}")
                error.printStackTrace()
                completionHandler(null)
            }) {
            @Throws(AuthFailureError::class)
            override fun getHeaders(): Map<String, String> {
                val headers = HashMap<String, String>()
                headers.put("Content-Type", "application/json")
                return headers
            }
        }
        VolleyLog.d(TAG, jsonObjReq.toString())
        SleepRecordingRestApi.instance?.addToRequestQueue(jsonObjReq, TAG)
    }
}
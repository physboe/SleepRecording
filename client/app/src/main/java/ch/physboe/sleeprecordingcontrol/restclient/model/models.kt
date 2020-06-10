package ch.physboe.sleeprecordingcontrol.restclient.model

import com.google.gson.annotations.SerializedName
import java.io.Serializable

class RecordingState (
    val running: Boolean,
    val tag: String
)
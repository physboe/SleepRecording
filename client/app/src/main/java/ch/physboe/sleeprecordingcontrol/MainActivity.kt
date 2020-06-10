package ch.physboe.sleeprecordingcontrol

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import ch.physboe.sleeprecordingcontrol.restclient.SleepRecordingService
import ch.physboe.sleeprecordingcontrol.restclient.SleepRecordingWebService
import ch.physboe.sleeprecordingcontrol.restclient.model.RecordingState
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.gson.Gson
import org.json.JSONObject


class MainActivity : AppCompatActivity() {

    companion object{
        val TAG = MainActivity::class.java.simpleName
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val navView: BottomNavigationView = findViewById(R.id.nav_view)

        val navController = findNavController(R.id.nav_host_fragment)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(setOf(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications))
        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)

    }

    override fun onStart() {
        super.onStart()
        val button: Button = findViewById(R.id.button_toogle_recording)
        val controlService = SleepRecordingService()
        button.isEnabled = false
        button.isClickable = false

        controlService.getRecordingState { recordingState ->
            if(recordingState != null) {
                Toast.makeText(applicationContext,getString(R.string.connected), Toast.LENGTH_SHORT).show()
                changeButton(recordingState, button)
            } else {
                Toast.makeText(applicationContext,getString(R.string.not_conntected), Toast.LENGTH_LONG).show()
            }
        }
    }

    fun toggleStartRecording(view : View) {
        val button: Button = findViewById(R.id.button_toogle_recording);
        val controlService = SleepRecordingService()
        button.isEnabled = false
        button.isClickable = false
        controlService.getRecordingState { recordingState ->
            if(recordingState != null ) {
                val request = RecordingState(!recordingState.running, "night")
                controlService.putRecordingState(request){
                    controlService.getRecordingState { recordingState ->
                        if(recordingState!=null){
                            changeButton(recordingState, button)
                        }
                    }

                }
            } else {
                Toast.makeText(applicationContext,getString(R.string.not_conntected), Toast.LENGTH_LONG).show()
            }
        }

    }

    private fun changeButton(recordingState: RecordingState, button : Button){
        if (recordingState.running) {
            button.text = getString(R.string.text_button_stop_recording)
        } else {
            button.text = getString(R.string.text_button_start_recording)
        }
        button.isEnabled = true
        button.isClickable = true
    }
}
package com.example.groupfitandroidapp;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.widget.TextView;

public class SensorService implements SensorEventListener {

    private final Sensor mHeartRateSensor;
    private final SensorManager mSensorManager;

    private Context context;
    private String sessionName;

    private final TextView textView;

    private int sendHttp=1;



    public SensorService(Context context, TextView text, String sessionName) {
        mSensorManager =  (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        mHeartRateSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE);
        mSensorManager.registerListener(this, mHeartRateSensor, SensorManager.SENSOR_DELAY_NORMAL);
        this.textView = text;
        this.context = context;
        this.sessionName = sessionName;
    }
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {

        sendHttp++;

        if ((sendHttp%6) == 0) {
            //limit time sending data to server
            sendHttp = 1;
            float heartRate = sensorEvent.values[0];
            System.out.println("HeartRate ");
            System.out.println(heartRate);

            textView.setText("Heart Rate: " + heartRate + " bpm");

            //Post update to server
            String body = "{\"datatype\":\"" + "HEARTRATE" + "\",\"value\":" + heartRate + ",\"watch_id\":\"" + UUIDManager.getUUID(context) + "\",\"workout_session_name\":\"" + sessionName + "\",\"timestamp\":\"" + System.currentTimeMillis() + "\"}";
            System.out.println("BODY");
            System.out.println(body);
            HttpService.sendPostRequest(body, "/send-workout-data",
                    jsonResponse -> {
                        //do whatever has to be done on success
                    }, error -> {
                        error.printStackTrace();
                    }

            );
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }


    public void stop() {
        this.mSensorManager.unregisterListener(this,mHeartRateSensor);
    }
}

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



    public SensorService(Context context, TextView text) {
        mSensorManager =  (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        mHeartRateSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE);
        mSensorManager.registerListener(this, mHeartRateSensor, 5);
        this.textView = text;
        this.context = context;
    }
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {

        float heartRate = sensorEvent.values[0];
        System.out.println("HeartRate ");
        System.out.println(heartRate);

        textView.setText("Heart Rate: " + heartRate + " bpm");

        //Post update to server
        String body = "{\"datatype\":\"" + "HEARTRATE" + "\",\"value\":" + heartRate + ",\"watch_id\":\"" + UUIDManager.getUUID(context) + "\",\"workout_session_name\":\"" + this.sessionName + "\",\"timestamp\":\"" + System.currentTimeMillis() + "\"}";
        HttpService.sendPostRequest(body, "/send-workout-data",
                jsonResponse -> {
                    //do whatever has to be done on success
                }, error -> {
                    error.printStackTrace();
                }

        );

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}

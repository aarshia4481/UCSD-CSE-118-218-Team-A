package com.example.groupfitandroidapp;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.widget.TextView;

import com.google.firebase.crashlytics.buildtools.api.net.Constants;

import org.w3c.dom.Text;

public class SensorService implements SensorEventListener {

    private Sensor mHeartRateSensor;
    private SensorManager mSensorManager;
    private HttpService client;

    private TextView textView;



    public SensorService(Context context, HttpService client, TextView text) {
        mSensorManager =  (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
        mHeartRateSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE);
        mSensorManager.registerListener(this, mHeartRateSensor, 5);
        this.client = client;
        this.textView = text;
    }
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {

        float heartRate = sensorEvent.values[0];
        System.out.println("HeartRate ");
        System.out.println(heartRate);


        textView.setText("Heart Rate: " + heartRate + " bpm");


        //Post update to server
        // @Todo send data in right format to backend server
        // client.sendPostRequest("{\"heartRate\": \"" + heartRate  + "\"}", "/post-workout-data");

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}

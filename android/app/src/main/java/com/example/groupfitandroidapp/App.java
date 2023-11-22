package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.health.services.client.ExerciseClient;
import androidx.health.services.client.HealthServices;
import androidx.health.services.client.HealthServicesClient;
import androidx.health.services.client.data.Availability;
import androidx.health.services.client.data.DataType;
import androidx.health.services.client.data.ExerciseCapabilities;
import androidx.health.services.client.data.ExerciseConfig;
import androidx.health.services.client.data.ExerciseLapSummary;
import androidx.health.services.client.data.ExerciseType;
import androidx.health.services.client.data.ExerciseConfig;
import androidx.health.services.client.data.ExerciseTypeCapabilities;
import androidx.health.services.client.data.ExerciseUpdate;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.firebase.crashlytics.buildtools.api.net.Constants;

import java.io.IOException;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;


public class App extends Activity {



    private ExerciseConfig.Builder exerciseConfigBuilder;
    HttpService client = new HttpService();



    private TextView heartRateTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        //setContentView(R.layout.session_selection_view);


        System.out.println("Running onCreate function...");
        setContentView(R.layout.activity_main);

        heartRateTextView = findViewById(R.id.textViewHeartRate);


        // Create WebSocket connection
        //get userID
        String uuid = UUIDManager.getUUID(getApplicationContext());



        String data = "{\"user\": \"" + uuid  + "\"}";


        // Try to send POST request
        client.sendPostRequest(data,  new HttpService.Callback() {

            @Override
            public void onSuccess() {
                System.out.println("Success sending POST request");
            }

            @Override
            public void onError(String errorMessage) {

            }

        });

        //Try to access sensor data
        Context context = getApplicationContext();
        SensorService heartRate = new SensorService(context, client, heartRateTextView);

        final HealthServicesClient healthClient = HealthServices.getClient(this.getApplicationContext());
        final ExerciseClient exerciseClient = healthClient.getExerciseClient();

        ExerciseType exerciseType = ExerciseType.SQUAT;
        exerciseConfigBuilder = ExerciseConfig.builder(exerciseType);

        //Everything after this is related to healt services API
        /*ListenableFuture<ExerciseCapabilities> capabilitiesListenableFuture =  exerciseClient.getCapabilitiesAsync();

        Futures.addCallback(capabilitiesListenableFuture, new
        FutureCallback<ExerciseCapabilities>() {
            @Override
            public void onSuccess(@Nullable ExerciseCapabilities result) {
                try {
                    ExerciseTypeCapabilities exerciseTypeCapabilities =
                            result.getExerciseTypeCapabilities(exerciseType);
                    Set<DataType<?, ?>> exerciseCapabilitiesSet =
                            exerciseTypeCapabilities.getSupportedDataTypes();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onFailure(Throwable t) {

            }
        }, Executors.newSingleThreadExecutor());

        exerciseConfigBuilder = ExerciseConfig.builder(exerciseType);*/


/*        ExerciseUpdateListener exerciseUpdateListener =
                new ExerciseUpdateListener() {
                    @Override
                    public void onExerciseUpdate(ExerciseUpdate update) {
                        updateRepCount(update);
                    }

                    @Override
                    public void onLapSummary(ExerciseLapSummary summary) {
                        //Processing Lap Summary
                    }
                };


        ListenableFuture<Void> startExerciseListenableFuture = exerciseClient.startExercise(exerciseConfigBuilder.build());
        ListenableFuture<Void> updateListenableFuture = exerciseClient.setUpdateListener(exerciseUpdateListener);


    }*/

   /* @Override
    protected void onResume() {
        super.onResume();
    }

    public void onExerciseUpdate(@NonNull ExerciseUpdate update) {
        try {
            updateRepCount(update);
        } catch (Exception exception) {
            Log.e("Error getting exercise update: ", exception.toString());
        }
    }

    private void updateRepCount(ExerciseUpdate update) {
        System.out.println(update);
*/
    }

}
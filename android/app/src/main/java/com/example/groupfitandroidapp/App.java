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
import androidx.core.content.ContextCompat;
import androidx.health.services.client.ExerciseClient;
import androidx.health.services.client.ExerciseUpdateListener;
import androidx.health.services.client.HealthServices;
import androidx.health.services.client.HealthServicesClient;
import androidx.health.services.client.data.Availability;
import androidx.health.services.client.data.DataPoint;
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
import java.util.List;
import java.util.Set;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;


public class App extends Activity {



    private ExerciseConfig.Builder exerciseConfigBuilder;
  //  HttpService client = new HttpService();



    private TextView heartRateTextView;
    private TextView repCounterTextView;

    private HealthServicesClient healthClient;
    private ExerciseClient exerciseClient;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        //setContentView(R.layout.session_selection_view);


        System.out.println("Running onCreate function...");
        setContentView(R.layout.activity_main);

        heartRateTextView = findViewById(R.id.textViewHeartRate);
        repCounterTextView = findViewById(R.id.textViewRepCounter);

        // Create WebSocket connection
        //get userID
        String uuid = UUIDManager.getUUID(getApplicationContext());


        String data = "{\"user\": \"" + uuid + "\"}";

        HttpService.sendPostRequest(data);

    }


    @Override
    protected void onStart() {
        super.onStart();

        healthClient = HealthServices.getClient(this.getApplicationContext());
        exerciseClient = healthClient.getExerciseClient();

    }

    @Override
    protected void onResume() {
        super.onResume();

        //Try to access sensor data
        Context context = getApplicationContext();
        //SensorService heartRate = new SensorService(context, client, heartRateTextView);


        ExerciseType exerciseType = ExerciseType.SQUAT;


        //Everything after this is related to health services API
        ListenableFuture<ExerciseCapabilities> capabilitiesListenableFuture =  exerciseClient.getCapabilities();

        Futures.addCallback(capabilitiesListenableFuture, new
                FutureCallback<ExerciseCapabilities>() {
                    @Override
                    public void onSuccess(@Nullable ExerciseCapabilities result) {
                        Boolean capabilities  = result.getSupportedExerciseTypes()
                                .contains(ExerciseType.SQUAT);
                    }

                    @Override
                    public void onFailure(Throwable t) {
                        // display an error
                    }
                },  ContextCompat.getMainExecutor(this));




        ExerciseUpdateListener exerciseUpdateListener =
                new ExerciseUpdateListener() {

                    @Override
                    public void onAvailabilityChanged(@NonNull DataType dataType, @NonNull Availability availability) {

                    }

                    public void onExerciseUpdate(ExerciseUpdate update) {
                        updateRepCount(update);
                    }

                    @Override
                    public void onLapSummary(ExerciseLapSummary summary) {
                        //Processing Lap Summary
                    }
                };

        ExerciseConfig config = ExerciseConfig.builder().setExerciseType(exerciseType).build();

        ListenableFuture<Void> startExerciseListenableFuture =  exerciseClient.startExercise(config);
        ListenableFuture<Void> updateListenableFuture = exerciseClient.setUpdateListener(exerciseUpdateListener);


    }


    private void updateRepCount(ExerciseUpdate update) {

        List<DataPoint> rep_count = update.getLatestMetrics().get(DataType.REP_COUNT);
        if (rep_count != null) {
            long reps = rep_count.get(0).getValue().asLong();
            System.out.println(reps);
            repCounterTextView.setText("Rep counter: " + reps);
        }




    }

}
//start app, join session and create session
//for join session - automatically go to the heart rate and r
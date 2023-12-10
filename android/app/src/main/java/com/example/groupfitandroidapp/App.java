package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
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
import androidx.health.services.client.data.ExerciseUpdate;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;

import java.util.List;


public class App extends Activity {
    private ExerciseConfig.Builder exerciseConfigBuilder;
    private TextView heartRateTextView;
    private TextView repCounterTextView;
    private TextView exerciseTypeTextView;
    private HealthServicesClient healthClient;
    private ExerciseClient exerciseClient;
    private String sessionName;
    private ExerciseType exerciseType;
    private SensorService heartRateSensor;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        Intent intent = getIntent();
        sessionName = intent.getStringExtra("sessionName");

        super.onCreate(savedInstanceState);
        //setContentView(R.layout.session_selection_view);


        System.out.println("Running onCreate function...");
        setContentView(R.layout.activity_main);

        heartRateTextView = findViewById(R.id.textViewHeartRate);
        repCounterTextView = findViewById(R.id.textViewRepCounter);
        exerciseTypeTextView = findViewById(R.id.textViewExerciseType);

        //get userID
        String uuid = UUIDManager.getUUID(getApplicationContext());



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
        heartRateSensor = new SensorService(context, heartRateTextView, sessionName);


        exerciseType = ExerciseType.SQUAT;

        exerciseTypeTextView.setText(exerciseType.toString());


        //Everything after this is related to health services API
        ListenableFuture<ExerciseCapabilities> capabilitiesListenableFuture =  exerciseClient.getCapabilities();

        Futures.addCallback(capabilitiesListenableFuture, new
                FutureCallback<ExerciseCapabilities>() {
                    @Override
                    public void onSuccess(@Nullable ExerciseCapabilities result) {
                        Boolean capabilities  = result.getSupportedExerciseTypes()
                                .contains(exerciseType);
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
                        System.out.println("Lap completed: " + summary);
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
            repCounterTextView.setText("Rep counter: " + reps);


            //send data to server
            String exerciseType_str = String.valueOf(exerciseType);
            String workoutSessionId = "";

            String exerciseLogJson = "{\"datatype\":\"" + exerciseType_str + "\",\"value\":" + reps + ",\"watch_id\":\"" + UUIDManager.getUUID(getApplicationContext()) + "\",\"workout_session_name\":\"" + sessionName + "\",\"timestamp\":\"" + System.currentTimeMillis() + "\"}";
            HttpService.sendPostRequest(exerciseLogJson, "/send-workout-data",
            jsonResponse -> {
                //do whatever has to be done on success
            }, error -> {
                error.printStackTrace();
                    }

            );
        }

    }


    @Override
    protected void onStop() {

        super.onStop();
        ListenableFuture<Void> endExerciseListenableFuture =  exerciseClient.endExercise();
        heartRateSensor.stop();

    }

}

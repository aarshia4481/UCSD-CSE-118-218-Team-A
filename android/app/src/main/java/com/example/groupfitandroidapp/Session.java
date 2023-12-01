package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
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

public class Session extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.session_selection_view);
        Button joinButton = findViewById(R.id.button2);
        Button createButton = findViewById(R.id.button3);
        joinButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                // Create an Intent to start the new activity
                Intent intent = new Intent(Session.this, App.class);

                // Start the new activity
                startActivity(intent);
        }});
    }
}
package com.example.groupfitandroidapp;

import static java.lang.Thread.sleep;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.HashMap;
import java.util.Map;

public class waitForUsers extends Activity {


    private final Handler handler = new Handler(Looper.getMainLooper());
    Boolean queryParticpants = false;


        @Override
        protected void onCreate(Bundle savedInstanceState) {

            super.onCreate(savedInstanceState);
            setContentView(R.layout.waiting_for_participants);
            Button buttonStart = findViewById(R.id.buttonStart);
            buttonStart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {

                    //send start to server

                    Intent intent = new Intent(waitForUsers.this, App.class);
                    // Start the new activity
                    startActivity(intent);
                    queryParticpants=false;

                }
            });

            queryParticpants=true;
            getParticipants();
        }

    private void getParticipants() {
        Map<String, String> params = new HashMap<>();
        params.put("test", "test");

        new Thread(() -> {
            while (queryParticpants) {
                // send get request to see if other users joined session
                HttpService.sendGetRequest("/get-sessions", params,
                        jsonResponse -> {
                            System.out.println("GET request successful");
                            System.out.println(jsonResponse);

                            // Process the jsonResponse here
                            String response = "Joined: " + jsonResponse; // Modify as needed

                            // Update UI using the handler
                            handler.post(() -> {
                                TextView textViewParticipants = findViewById(R.id.countParticipants);
                                textViewParticipants.setText(response); // Update TextView with processed data
                            });
                        },
                        error -> {
                            error.printStackTrace();
                        }
                );

                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }




        protected void onResume() {
            super.onResume();
        }



}

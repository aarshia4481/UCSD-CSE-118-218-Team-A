package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.HashMap;
import java.util.Map;

public class waitForUsers extends Activity {


    private final Handler handler = new Handler(Looper.getMainLooper());
    private Boolean queryParticpants = false;
    private String sessionName;


        @Override
        protected void onCreate(Bundle savedInstanceState) {

            super.onCreate(savedInstanceState);
            setContentView(R.layout.waiting_for_participants);
            Button buttonStart = findViewById(R.id.buttonStart);
            Intent intent = getIntent();
            sessionName = intent.getStringExtra("sessionName");

            buttonStart.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {

                    //send start to server
                    String body = "{\"session_name\":\"" + sessionName + "\"}";

                    HttpService.sendPostRequest(body, "/get-participants", jsonResponse -> {

                    }, error -> {
                        error.printStackTrace();
                    });

                    Intent next_intent = new Intent(waitForUsers.this, App.class);
                    next_intent.putExtra("sessionName", sessionName);
                    // Start the new activity
                    startActivity(next_intent);
                    queryParticpants=false;

                }
            });

            queryParticpants=true;
            getParticipants();
        }

    private void getParticipants() {
        Map<String, String> params = new HashMap<>();
        params.put("session_name", sessionName);

        new Thread(() -> {
            while (queryParticpants) {
                // send get request to see if other users joined session
                HttpService.sendGetRequest("/get-participants", params,
                        jsonResponse -> {
                            System.out.println("GET request successful");
                            System.out.println(jsonResponse);
                            int count_participants = 0;
                            try {
                                JSONArray participants = jsonResponse.getJSONArray("participants");
                                count_participants = participants.length();

                            } catch (JSONException e) {
                                throw new RuntimeException(e);
                            }

                            // Process the jsonResponse here
                            String response = "Joined: " + count_participants; // Modify as needed

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

package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;

public class joinSession extends Activity {

    private String sessionName;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.join_session);
        final EditText editTextName = findViewById(R.id.editTextName2);
        Button buttonSubmit = findViewById(R.id.buttonSubmit2);
        buttonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Get the entered name
                String enteredName = editTextName.getText().toString();

                // Create an intent to send the result back to the calling activity
                // Create an Intent to start the new activity
                String uuid = UUIDManager.getUUID(getApplicationContext());
                String params = "{\"session_name\":\"" + enteredName + "\",\"user_id\":\"" + uuid
                + "\"}";

                HttpService.sendPostRequest(params, "/join-session",
                        jsonResponse -> {

                            // on success
                            System.out.println("TEST2");
                            System.out.println(jsonResponse);
                            try {
                                sessionName = jsonResponse.getString("session_name");
                            } catch (JSONException e) {
                                throw new RuntimeException(e);
                            }

                            System.out.println("TEST: " + sessionName);
                            Intent intent = new Intent(joinSession.this, waitForUsers.class);
                            intent.putExtra("sessionName", sessionName);

                            // Start the new activity
                            startActivity(intent);

                            finish();

                        }, error -> {
                        //onError
                            System.out.println(error.getStackTrace());
                        }

                        );


            }
        });

    }

}





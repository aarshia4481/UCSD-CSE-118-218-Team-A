package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;

public class createSession extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.create_session);
        final EditText editTextName = findViewById(R.id.editTextName);
        Button buttonSubmit = findViewById(R.id.buttonSubmit);
        buttonSubmit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Get the entered name
                String enteredName = editTextName.getText().toString();

                // Create an intent to send the result back to the calling activity
                // Create an Intent to start the new activity
                String uuid = UUIDManager.getUUID(getApplicationContext());
                String exerciseLogJson = "{\"session_name\":\"" + enteredName + "\",\"creator_id\":\"" + uuid
                        + "\"}";
                HttpService.sendPostRequest(exerciseLogJson, "/create-session",
                        jsonResponse -> {
                            //onSuccess

                            String sessionName;
                            try {
                                sessionName = jsonResponse.get("session_name").toString();
                            } catch (JSONException e) {
                                throw new RuntimeException(e);
                            }

                            System.out.println(sessionName);
                            Intent intent = new Intent(createSession.this, waitForUsers.class);
                            // pass on sessionName to next activity
                            intent.putExtra("sessionName", sessionName);
                            startActivity(intent);

                        },
                        error -> {
                            error.printStackTrace();
                        }

                );


//                Intent resultIntent = new Intent();
//                resultIntent.putExtra("name", enteredName);
//
//                // Set the result and finish the activity
//                setResult(Activity.RESULT_OK, resultIntent);
//                finish();
            }
        });


    }


    protected void onResume() {
        super.onResume();


    }
}





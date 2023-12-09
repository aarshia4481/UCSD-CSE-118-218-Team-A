package com.example.groupfitandroidapp;

import static java.lang.Thread.sleep;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.firebase.crashlytics.buildtools.api.net.Constants;

import java.util.HashMap;
import java.util.Map;

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
                            //@ToDo save the returned session_id somewhere
                            // the json looks like this:
                            // {"session_name": "My 11 session", "creator_id": "eyJhbGciOiJSU0EtT0FF", "participants": [], "session_id":
                            //"d3c403fb-4dcc-4854-84e6-eb15838d4c7d", "state": "created", "_id": "656fd61ce8a1af49a673e931"}


                        },
                        error -> {
                            error.printStackTrace();
                        }

                );






               Intent intent = new Intent(createSession.this, waitForUsers.class);
               // Start the new activity
              startActivity(intent);

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





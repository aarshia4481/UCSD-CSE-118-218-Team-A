package com.example.groupfitandroidapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class Session extends Activity {
    Button createButton;
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
                Intent intent = new Intent(Session.this, joinSession.class);

                // Start the new activity
                startActivity(intent);
            }});

        createButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                // Create an Intent to start the new activity
                Intent intent = new Intent(Session.this, createSession.class);

                // Start the new activity
                startActivity(intent);
            }});
    }

}

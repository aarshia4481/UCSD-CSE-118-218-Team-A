package com.example.groupfitandroidapp;


import android.content.Context;
import android.content.SharedPreferences;

import java.util.UUID;

    public class UUIDManager {
        private static final String PREF_UNIQUE_ID = "PREF_UNIQUE_ID";
        private static String uniqueID = null;

        public synchronized static String getUUID(Context context) {
            if (uniqueID == null) {
                SharedPreferences sharedPreferences = context.getSharedPreferences(
                        PREF_UNIQUE_ID, Context.MODE_PRIVATE);
                uniqueID = sharedPreferences.getString(PREF_UNIQUE_ID, null);

                if (uniqueID == null) {
                    uniqueID = UUID.randomUUID().toString();
                    SharedPreferences.Editor editor = sharedPreferences.edit();
                    editor.putString(PREF_UNIQUE_ID, uniqueID);
                    editor.apply();
                }
            }
            return uniqueID;
        }
    }


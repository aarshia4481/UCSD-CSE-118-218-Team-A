package com.example.groupfitandroidapp;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HttpService {

    private static final URL url; // Replace with your Flask server URL

    static {
        try {

            url = new URL("https://94a9-137-110-116-189.ngrok-free.app/post");
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
    }

    private static final ExecutorService executor = Executors.newSingleThreadExecutor();

    public static void sendPostRequest(final String jsonData, final Callback callback) {
        executor.execute(() -> {
            HttpURLConnection con = null;
            try {
                con = (HttpURLConnection) url.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Content-Type", "application/json");
                con.setRequestProperty("Accept", "application/json");
                con.setDoOutput(true);

                try (OutputStream os = con.getOutputStream()) {
                    byte[] input = jsonData.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = con.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    callback.onSuccess(); // Notify success
                } else {
                    callback.onError("HTTP Error: " + responseCode); // Notify error
                }
            } catch (IOException e) {
                callback.onError(e.getMessage()); // Notify error
            } finally {
                if (con != null) {
                    con.disconnect();
                }
            }
        });
    }

    public interface Callback {
        void onSuccess();

        void onError(String errorMessage);
    }
}

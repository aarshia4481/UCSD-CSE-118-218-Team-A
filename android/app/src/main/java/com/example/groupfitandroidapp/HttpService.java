package com.example.groupfitandroidapp;

import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HttpService {

    static String url = "https://5067-69-196-44-85.ngrok-free.app";
    private static final ExecutorService executor = Executors.newSingleThreadExecutor();

    public static void sendPostRequest(final String jsonData, String endpoint, Callback<JSONObject> onResponse, Callback<Exception> onError) {
        executor.execute(() -> {
            HttpURLConnection con = null;
            URL finalUrl;
            try {
                finalUrl = new URL(url + endpoint);
                con = (HttpURLConnection) finalUrl.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Content-Type", "application/json");
                con.setRequestProperty("Accept", "application/json");
                con.setDoOutput(true);

                // Send data
                try (OutputStream os = con.getOutputStream()) {
                    byte[] input = jsonData.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                // Get response code
                int responseCode = con.getResponseCode();
                System.out.println("Response Code: " + responseCode);

                // Read the response body if the request was successful (status code 200)
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                    String inputLine;
                    StringBuilder response = new StringBuilder();

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();

                    // Print the response body
                    System.out.println("Response Body: " + response.toString());

                    // Parse JSON response
                    try {
                        JSONObject jsonObject = new JSONObject(response.toString());
                        onResponse.execute(jsonObject); // Pass the JSON object through the callback
                    } catch (Exception e) {
                        onError.execute(e); // Handle JSON parsing error
                    }
                } else {
                    System.out.println("Error in HTTP request, response code: " + responseCode);
                    onError.execute(new RuntimeException("HTTP Error: " + responseCode)); // Pass error through the callback
                }
            } catch (MalformedURLException e) {
                onError.execute(e); // Pass URL error through the callback
            } catch (IOException e) {
                onError.execute(e); // Pass IO error through the callback
            } finally {
                if (con != null) {
                    con.disconnect();
                }
            }
        });
    }

    public interface Callback<T> {
        void execute(T response);
    }
}

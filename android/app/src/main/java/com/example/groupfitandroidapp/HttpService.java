package com.example.groupfitandroidapp;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HttpService {

    static String url = "https://groupfit-server.fly.dev";

    //local
    //static String url =  "https://64c5-137-110-116-189.ngrok-free.app";
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
                    byte[] input = jsonData.getBytes(StandardCharsets.UTF_8);
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
                    System.out.println("Response Body: " + response);

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


    public static void sendGetRequest(final String endpoint, Map<String, String> params, Callback<JSONObject> onResponse, Callback<Exception> onError) {
        executor.execute(() -> {
            HttpURLConnection con = null;
            try {
                StringBuilder urlString = new StringBuilder(url + endpoint);

                // Append parameters to the URL
                if (params != null && !params.isEmpty()) {
                    urlString.append("?");
                    for (Map.Entry<String, String> entry : params.entrySet()) {
                        urlString.append(URLEncoder.encode(entry.getKey(), "UTF-8"))
                                .append("=")
                                .append(URLEncoder.encode(entry.getValue(), "UTF-8"))
                                .append("&");
                    }
                    urlString.deleteCharAt(urlString.length() - 1); // Remove the trailing "&"
                }

                URL finalUrl = new URL(urlString.toString());
                con = (HttpURLConnection) finalUrl.openConnection();
                con.setRequestMethod("GET");
                con.setRequestProperty("Accept", "application/json");

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
                    System.out.println("Response Body: " + response);

                    // Parse JSON response
                    try {
                        JSONObject jsonObject = new JSONObject(response.toString());
                        onResponse.execute(jsonObject); // Pass the JSON object through the callback
                    } catch (Exception e) {
                        //@ToDo what if the response is no JSON? For now just create an empty object so the onSUccess callback is still called.
                        onResponse.execute(new JSONObject()); // Handle JSON parsing error
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

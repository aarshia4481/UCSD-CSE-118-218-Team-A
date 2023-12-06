package com.example.groupfitandroidapp;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HttpService {



    static String url = "https://5067-69-196-44-85.ngrok-free.app";


    private static final ExecutorService executor = Executors.newSingleThreadExecutor();

    public static void sendPostRequest(final String jsonData, String endpoint) {
        executor.execute(() -> {
            HttpURLConnection con = null;
            URL final_url;
            try {
                final_url = new URL(url + endpoint );
            } catch (MalformedURLException e) {
                throw new RuntimeException(e);
            }
            try {
                con = (HttpURLConnection) final_url.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Content-Type", "application/json");
                con.setRequestProperty("Accept", "application/json");
                con.setDoOutput(true);

                try (OutputStream os = con.getOutputStream()) {
                    byte[] input = jsonData.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = con.getResponseCode();
                System.out.println(responseCode);


            } catch (IOException e) {
                System.out.println(e.getStackTrace());

            } finally {
                if (con != null) {
                    con.disconnect();
                }
            }
        });
    }

}
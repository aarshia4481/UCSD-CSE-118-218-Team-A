plugins {
    id("com.android.application")
}

android {
    namespace = "com.example.groupfitandroidapp"
    compileSdk = 33

    defaultConfig {
        applicationId = "com.example.groupfitandroidapp"
        minSdk = 30
        targetSdk = 33
        versionCode = 1
        versionName = "1.0"

    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

dependencies {

    implementation("com.google.android.gms:play-services-wearable:18.1.0")
    implementation("androidx.percentlayout:percentlayout:1.0.0")
    implementation("androidx.legacy:legacy-support-v4:1.0.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    implementation("androidx.health:health-services-client:1.0.0-beta03")

    // To use CallbackToFutureAdapter
    implementation("androidx.concurrent:concurrent-futures:1.1.0")

    // Kotlin
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-guava:1.6.0")
    implementation("com.google.firebase:firebase-crashlytics-buildtools:2.9.9")

    configurations.all {
        resolutionStrategy {
            force("org.jetbrains.kotlin:kotlin-stdlib:1.5.31")
            force("org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.5.31")
        }
    }

}
package com.example.snarkyoverlay;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;

public class MainActivity extends Activity {

    private static final int REQUEST_CODE_OVERLAY_PERMISSION = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(android.view.Gravity.CENTER);

        Button btnPermission = new Button(this);
        btnPermission.setText("Grant Overlay Permission");
        btnPermission.setOnClickListener(v -> checkOverlayPermission());

        Button btnAccessibility = new Button(this);
        btnAccessibility.setText("Enable Snarky Service");
        btnAccessibility.setOnClickListener(v -> openAccessibilitySettings());

        layout.addView(btnPermission);
        layout.addView(btnAccessibility);

        setContentView(layout);
    }

    private void checkOverlayPermission() {
        if (!Settings.canDrawOverlays(this)) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:" + getPackageName()));
            startActivityForResult(intent, REQUEST_CODE_OVERLAY_PERMISSION);
        } else {
            Toast.makeText(this, "Overlay permission already granted!", Toast.LENGTH_SHORT).show();
        }
    }

    private void openAccessibilitySettings() {
        Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
        startActivity(intent);
        Toast.makeText(this, "Find 'Snarky Assistant' and enable it.", Toast.LENGTH_LONG).show();
    }
}

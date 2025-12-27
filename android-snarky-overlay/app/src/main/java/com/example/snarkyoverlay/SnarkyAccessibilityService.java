package com.example.snarkyoverlay;

import android.accessibilityservice.AccessibilityService;
import android.graphics.PixelFormat;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.TextView;
import android.util.Log;

public class SnarkyAccessibilityService extends AccessibilityService {

    private WindowManager windowManager;
    private View overlayView;
    private TextView snarkyTextView;
    private Handler handler = new Handler(Looper.getMainLooper());
    private static final String TAG = "SnarkyService";

    // Rate limiting to avoid constant updates
    private long lastUpdate = 0;
    private static final long UPDATE_INTERVAL_MS = 3000;

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Log.d(TAG, "Service Connected");
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
        createOverlay();
    }

    private void createOverlay() {
        if (overlayView != null) return;

        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
                PixelFormat.TRANSLUCENT);

        params.gravity = Gravity.TOP | Gravity.START;
        params.x = 100;
        params.y = 200;

        LayoutInflater inflater = LayoutInflater.from(this);
        overlayView = inflater.inflate(R.layout.overlay_layout, null);
        snarkyTextView = overlayView.findViewById(R.id.snarky_text);

        try {
            windowManager.addView(overlayView, params);
        } catch (Exception e) {
            Log.e(TAG, "Error adding view: " + e.getMessage());
        }

        // Setup simple drag (optional, simple implementation)
        overlayView.setOnTouchListener(new View.OnTouchListener() {
            private int initialX;
            private int initialY;
            private float initialTouchX;
            private float initialTouchY;

            @Override
            public boolean onTouch(View v, android.view.MotionEvent event) {
                switch (event.getAction()) {
                    case android.view.MotionEvent.ACTION_DOWN:
                        initialX = params.x;
                        initialY = params.y;
                        initialTouchX = event.getRawX();
                        initialTouchY = event.getRawY();
                        return true;
                    case android.view.MotionEvent.ACTION_MOVE:
                        params.x = initialX + (int) (event.getRawX() - initialTouchX);
                        params.y = initialY + (int) (event.getRawY() - initialTouchY);
                        windowManager.updateViewLayout(overlayView, params);
                        return true;
                }
                return false;
            }
        });
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (System.currentTimeMillis() - lastUpdate < UPDATE_INTERVAL_MS) {
            return;
        }

        if (event.getEventType() == AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED ||
            event.getEventType() == AccessibilityEvent.TYPE_VIEW_SCROLLED) {

            AccessibilityNodeInfo rootNode = getRootInActiveWindow();
            if (rootNode != null) {
                StringBuilder sb = new StringBuilder();
                extractText(rootNode, sb);
                String screenContent = sb.toString();

                if (!screenContent.isEmpty()) {
                    String remark = SnarkGenerator.getSnark(screenContent);
                    updateOverlay(remark);
                    lastUpdate = System.currentTimeMillis();
                }
                rootNode.recycle();
            }
        }
    }

    private void extractText(AccessibilityNodeInfo node, StringBuilder sb) {
        if (node == null) return;

        if (node.getText() != null) {
            sb.append(node.getText()).append(" ");
        }

        // Limit depth/breadth for performance in a real app
        int childCount = node.getChildCount();
        for (int i = 0; i < childCount; i++) {
            AccessibilityNodeInfo child = node.getChild(i);
            if (child != null) {
                extractText(child, sb);
                child.recycle();
            }
        }
    }

    private void updateOverlay(String text) {
        handler.post(() -> {
            if (snarkyTextView != null) {
                snarkyTextView.setText(text);
                // Simple animation effect could go here
                overlayView.setAlpha(1.0f);
                overlayView.animate().alpha(0.8f).setDuration(2000).start();
            }
        });
    }

    @Override
    public void onInterrupt() {
        Log.d(TAG, "Service Interrupted");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (overlayView != null && windowManager != null) {
            windowManager.removeView(overlayView);
        }
    }
}

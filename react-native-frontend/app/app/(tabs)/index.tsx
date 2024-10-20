import React, { useState, useRef, useEffect } from 'react';
import { View, Text, Pressable, StyleSheet, Alert, PanResponder, Animated } from 'react-native';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';

export default function TabOneScreen() {
  const colorScheme = useColorScheme();
  const [isCalling, setIsCalling] = useState(false);
  const slideValue = useRef(new Animated.Value(0)).current; // Create a ref for animated value
  const [timer, setTimer] = useState(5);
  const buttonWidth = 250; // Width of the emergency button

  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: (_, gestureState) => {
        return gestureState.dx > 20; // Start sliding when dragged right more than 20 pixels
      },
      onPanResponderMove: (_, gestureState) => {
        // Update the animated value based on gesture movement
        const newValue = Math.min(buttonWidth, gestureState.dx); // Limit sliding to button width
        slideValue.setValue(newValue); // Set the value of the animated variable
      },
      onPanResponderRelease: () => {
        // Slide is sufficient to cancel
        if (slideValue.__getValue() >= buttonWidth / 2) {
          Alert.alert('Call Cancelled', 'The emergency call has been cancelled.');
          setIsCalling(false);
          slideValue.setValue(0); // Reset slide position
        } else {
          // If not sufficiently slid, reset the position
          slideValue.setValue(0);
        }
      },
    })
  ).current;

  useEffect(() => {
    let countdown;
    if (isCalling && timer > 0) {
      countdown = setTimeout(() => setTimer((prev) => prev - 1), 1000);
    } else if (timer === 0) {
      setIsCalling(false);
    }

    return () => clearTimeout(countdown);
  }, [isCalling, timer]);

  const handleEmergencyPress = () => {
    setIsCalling(true);
    slideValue.setValue(0); // Reset slide position
    setTimer(5); // Reset the timer for the countdown
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
      <Text style={[styles.appName, { color: Colors[colorScheme].text }]}>guardian angel</Text>

      <View
        style={[styles.emergencyButtonContainer, { backgroundColor: Colors[colorScheme].tint }]}
        {...panResponder.panHandlers}
      >
        <Animated.View
          style={[
            styles.emergencyButton,
            { transform: [{ translateX: slideValue }] }, // Apply slide value to the button's x position
          ]}
        >
          <Pressable onPress={handleEmergencyPress}>
            <Text style={styles.buttonText}>Emergency Call</Text>
          </Pressable>
        </Animated.View>
      </View>

      {isCalling && (
        <View>
          <Text style={[styles.timerText, { color: Colors[colorScheme].text }]}>
            Calling in {timer}...
          </Text>
          <Text style={[styles.cancelText, { color: Colors[colorScheme].text }]}>
            Slide to Cancel
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 40,
  },
  emergencyButtonContainer: {
    width: 250,
    height: 60,
    borderRadius: 10,
    overflow: 'hidden', // Ensures that the button doesn't overflow the container
    position: 'relative', // Allows for absolute positioning of the button
    justifyContent: 'center',
  },
  emergencyButton: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backgroundColor: 'blue', // Change the color if needed
  },
  buttonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
  },
  timerText: {
    fontSize: 20,
    marginVertical: 10,
    textAlign: 'center',
  },
  cancelText: {
    fontSize: 16,
    textAlign: 'center',
  },
});

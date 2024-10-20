import React, { useState, useRef, useEffect } from 'react';
import { View, Text, Pressable, StyleSheet, Alert, PanResponder, Animated, Image } from 'react-native';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useNavigation } from '@react-navigation/native';
import * as Permissions from "expo-permissions";
import { Audio } from 'expo-av';
import axios from 'axios';


export default function TabOneScreen() {
  const colorScheme = useColorScheme();
  const permission = requestMicrophonePermission();
  const [isCalling, setIsCalling] = useState(false);
  const slideValue = useRef(new Animated.Value(0)).current; // Create a ref for animated value
  const [timer, setTimer] = useState(5);
  const buttonWidth = 250; // Width of the emergency button
  const navigation = useNavigation();

// Get the navigation object



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
      onPanResponderRelease: async () => {
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


    const handleEmergencyPress = async () => {
    await requestMicrophonePermission();
    const { status } = await Permissions.askAsync(Permissions.AUDIO_RECORDING);
    if (status !== 'granted') {
      Alert.alert('Microphone Permission', 'Sorry, we need microphone permissions to make this work!');
    }
  }


  async function startRecording() {
    try {
      const { recording } = await Audio.Recording.createAsync({
        android: {
          extension: '.wav',
          outputFormat: Audio.RecordingOptionsAndroid.OutputFormat.DEFAULT,
          encoding: Audio.RecordingOptionsAndroid.Encoding.PCM_16BIT,
          sampleRate: 16000,
          numberOfChannels: 1,
        },
      });
      setRecording(recording);
      return true;
    } catch (error) {
      console.error('Failed to start recording', error);
      return false;
    }
  }

  async function stopRecording() {
    if (recording) {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      console.log('Recording stopped and stored at', uri);
      await sendAudioToDispatch(xuri);
      setRecording(null);
    }
  }

  async function sendAudioToDispatch(uri: string | null) {
    if (!uri) {
      console.error('No URI provided for audio');
      return;
    }

    const formData = new FormData();

    formData.append('audio', {
      uri,
      name: 'audio.wav',
      type: 'audio/wav',
    } as any); // Cast to any if TypeScript is giving an error

    try {
      const response = await axios.post('http://10.42.159.255:8000/dispatch/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        Alert.alert('Success', 'Your audio has been sent to emergency services.');
      } else {
        console.error('Failed to dispatch audio', response.data);
        Alert.alert('Error', 'Failed to send audio to emergency services.');
      }
    } catch (error) {
      console.error('Error sending audio to API', error);
      Alert.alert('Error', 'An error occurred while sending audio.');
    }
  }
    return (
    <View style={[styles.container, { backgroundColor: Colors[colorScheme].background }]}>
      <Image
        source={require('./guardian_angels_bear.png')}  // Path to the local image
        style={styles.image}
      />
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
  image: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
  },
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

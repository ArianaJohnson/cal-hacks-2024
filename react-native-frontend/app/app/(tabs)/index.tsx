import React, { useState, useRef, useEffect } from 'react';
import { View, Text, Pressable, StyleSheet, Alert, PanResponder, Animated, Image } from 'react-native';
import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useNavigation } from '@react-navigation/native';
import { Accelerometer } from 'expo-sensors';
// import * as Font from 'expo-font';

export default function TabOneScreen() {
  const colorScheme = useColorScheme();
  const [isCalling, setIsCalling] = useState(false);
  const slideValue = useRef(new Animated.Value(0)).current; // Create a ref for animated value
  const [timer, setTimer] = useState(5);
  const buttonWidth = 250; // Width of the emergency button
  const navigation = useNavigation(); // Get the navigation object

  // Accelerometer
  const [{ x, y, z }, setData] = useState({
    x: 0,
    y: 0,
    z: 0,
  });
  const [subscription, setSubscription] = useState(null);
  const _subscribe = () => {
    setSubscription(Accelerometer.addListener(setData));
  };
  const _unsubscribe = () => {
    subscription && subscription.remove();
    setSubscription(null);
  };
  useEffect(() => {
    // Accelerometer
    Accelerometer.setUpdateInterval(200);

    Accelerometer.isAvailableAsync().then(isAvailable => {
      if (isAvailable) {
        _subscribe();
      } else {
        Alert.alert('Accelerometer not available on this device');
      }
    });
    return () => _unsubscribe();
  }, []);

  useEffect(() => {
    if (Math.sqrt(Math.abs(x) ** 2 + Math.abs(y) ** 2 + Math.abs(z) ** 2) > 2.5) {
      handleEmergencyPress();
    }
  }, [x]);

  // const [fontsLoaded, setFontsLoaded] = useState(false);

  // useEffect(() => {
  //   async function loadFonts() {
  //     await Font.loadAsync({
  //       'Newsreader': require('NewsReader.ttf'), // Adjust the path as needed
  //     });
  //     setFontsLoaded(true);
  //   }
  //   loadFonts();
  // }, []);

  // if (!fontsLoaded) {
  //   return <Text>Loading...</Text>; // Show loading or a fallback UI
  // }

  // State for image cycling
  const [images] = useState([
    require('./../../assets/images/panic1.png'), // Replace with actual image paths
    require('./../../assets/images/panic2.png'),
    require('./../../assets/images/panic3.png'),
  ]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

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
      navigation.navigate('emergency-response');
    }

    return () => clearTimeout(countdown);
  }, [isCalling, timer]);

  useEffect(() => {
    // Set up image cycling
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 700); // Change image every 700 milliseconds

    return () => clearInterval(interval); // Clear interval on component unmount
  }, [images]);

  const handleEmergencyPress = () => {
    setIsCalling(true);
    slideValue.setValue(0); // Reset slide position
    setTimer(5); // Reset the timer for the countdown
  };

  return (

    <View style={[styles.container, { backgroundColor: 'white' }]}>
      <Image
        source={require('./guardian_angels_bear.png')}  // Path to the local image
        style={[styles.image1, { marginBottom: -120 }]}
      />
      <Image
        source={require('./guardian_angel.png')}  // Path to the local image
        style={styles.image2}
      />

      <View
        style={[styles.emergencyButtonContainer, { backgroundColor: Colors[colorScheme].background }]}
        {...panResponder.panHandlers}
      >
        <Animated.View
          style={[
            styles.emergencyButton,
            { transform: [{ translateX: slideValue }] }, // Apply slide value to the button's x position
          ]}
        >
          <Pressable onPress={handleEmergencyPress}>

            <Image
              source={images[currentImageIndex]}  // Use the current image from state
              style={styles.panicImage}
            />

          </Pressable>
        </Animated.View>
      </View>

      {isCalling && (
        <View>
          <Text style={[styles.timerText, { color: 'black', fontFamily: 'NewsReader' }]}>
            Calling in {timer}...
          </Text>
          <Text style={[styles.cancelText, { color: 'black', fontFamily: 'NewsReader' }]}>
            Slide to Cancel
          </Text>
        </View>
      )}
      {!isCalling && (
        <View>
          <Image
            source={require('./descrip text.png')}  // Path to the local image
            style={styles.descrip_text}
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  panicImage: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
  },
  image1: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
  },

  image2: {
    width: 250,
    height: 250,
    marginBottom: 0,
    resizeMode: 'contain',
  },

  descrip_text: {
    marginTop: -90,
    bottom: 0,
    width: 250,
    height: 250,
    resizeMode: 'contain',
  },

  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 0,  // Ensure no extra padding at the top
    marginTop: 0,
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 40,
  },
  emergencyButtonContainer: {
    width: 3000,
    height: 200,
    borderRadius: 0,
    marginTop: -100,
    overflow: 'hidden', // Ensures that the button doesn't overflow the container
    position: 'relative', // Allows for absolute positioning of the button
    justifyContent: 'center',
  },
  emergencyButton: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    backgroundColor: 'white', // Changed this to white yee
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
    fontFamily: 'NewsReader',
  },
  cancelText: {
    fontSize: 16,
    textAlign: 'center',
    fontFamily: 'NewsReader',
  },
});

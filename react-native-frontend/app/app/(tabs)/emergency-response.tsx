import React, { useState } from 'react';
import { StyleSheet, Button, View, Image} from 'react-native';
import axios from 'axios';
import { Text } from '@/components/Themed';

export default function TabTwoScreen() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callApi = async () => {
    setLoading(true);
    setError(null); // Reset any previous errors

    try {
      const response = await axios.post('http://10.42.131.62:8000/begin-conversation/', {
        // Sample patient data; adjust as needed
        name: 'John Doe',
        age: 30,
        emergency_contact: {
          name: 'Jane Doe',
          phone: '123-456-7890',
        },
        medical_info: {
          medical_conditions: ['Asthma'],
          allergies: ['Peanuts'],
          medications: ['Inhaler'],
        },
      });
      
      console.log('Response:', response.data);
      // Optionally handle successful response (e.g., navigate or show a message)
    } catch (err) {
      console.error('Error calling API:', err);
      setError('Failed to create patient.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container} >
      <Text style={styles.title}>Emergency Dispatch Responder</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      {error && <Text style={styles.error}>{error}</Text>}
      <Image
            source={require('../../assets/images/emergencybubble.png')}  // Path to the local image
            style={styles.image}
          />
      <Button
        title={loading ? "Loading..." : "Simulate dispatch"}
        onPress={callApi}
        disabled={loading}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
  error: {
    color: 'red',
    marginBottom: 10,
  },
  image: {
    height: 300,
    width: 300,
    resizeMode: 'contain',
  }
});

import React, { useState } from 'react';
import { StyleSheet, Button, View, Image} from 'react-native';
import axios from 'axios';
import { Text } from '@/components/Themed';
export default function TabTwoScreen() {
  const [isBegin, setIsBegin] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callApi = async () => {
    if(!isBegin){
      try {
        const response = await axios.post('http://127.0.0.1:8000/begin_conversation/');
        
        console.log('Response:', response.data);
        // Optionally handle successful response (e.g., navigate or show a message)
      } catch (err) {
        console.error('Error calling API:', err);
        setError('Failed to create patient.');
      } finally {
        setLoading(false);
      }
      setIsBegin(true);
    } else {
      try {
        const response = await axios.post('http://127.0.0.1:8000/continue_conversation/');
        
        console.log('Response:', response.data);
        // Optionally handle successful response (e.g., navigate or show a message)
      } catch (err) {
        console.error('Error calling API:', err);
        setError('Failed to create patient.');
      } finally {
        setLoading(false);
      }
      setIsBegin(false);
    }
    setLoading(true);
    setError(null); // Reset any previous errors

  };

  return (
    <View style={styles.container} >
       <Image
        source={require('./emergency dispatch responder.png')}  // Ensure the path is correct
        style={styles.text}
      />
      <View style={styles.separator} Color='black' />
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
  text: {
    width: 350,
    height: 350,
    alignSelf: 'center',
    resizeMode: 'contain',
    marginBottom: -220,
    marginTop: -100
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'black',
    fontFamily: 'Newsreader',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
    color: 'black',
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
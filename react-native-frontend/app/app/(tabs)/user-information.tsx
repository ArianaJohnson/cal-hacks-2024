import React, { useState } from 'react';
import { StyleSheet, TextInput, Button, ScrollView } from 'react-native';
import { Text, View } from '@/components/Themed';

export default function TabTwoScreen() {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [emergencyContactName, setEmergencyContactName] = useState('');
  const [emergencyContactPhone, setEmergencyContactPhone] = useState('');
  const [medicalConditions, setMedicalConditions] = useState('');
  const [allergies, setAllergies] = useState('');
  const [medications, setMedications] = useState('');

  const handleSubmit = () => {
    const patientData = {
      name,
      age: parseInt(age),
      emergency_contact: {
        name: emergencyContactName,
        phone: emergencyContactPhone,
      },
      medical_info: {
        medical_conditions: medicalConditions.split(','),
        allergies: allergies ? allergies.split(',') : [],
        medications: medications ? medications.split(',') : [],
      },
    };
    console.log(patientData); // You can send this data to your FastAPI backend
    // Here, you can make a POST request to the backend API
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Patient Information Form</Text>

      <Text>Name</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter name"
        value={name}
        onChangeText={setName}
      />

      <Text>Age</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter age"
        value={age}
        keyboardType="numeric"
        onChangeText={setAge}
      />

      <Text>Emergency Contact Name</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter emergency contact name"
        value={emergencyContactName}
        onChangeText={setEmergencyContactName}
      />

      <Text>Emergency Contact Phone</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter emergency contact phone"
        value={emergencyContactPhone}
        keyboardType="phone-pad"
        onChangeText={setEmergencyContactPhone}
      />

      <Text>Medical Conditions (comma-separated)</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter medical conditions"
        value={medicalConditions}
        onChangeText={setMedicalConditions}
      />

      <Text>Allergies (comma-separated, optional)</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter allergies"
        value={allergies}
        onChangeText={setAllergies}
      />

      <Text>Medications (comma-separated, optional)</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter medications"
        value={medications}
        onChangeText={setMedications}
      />

      <Button title="Submit" onPress={handleSubmit} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginBottom: 10,
  },
});

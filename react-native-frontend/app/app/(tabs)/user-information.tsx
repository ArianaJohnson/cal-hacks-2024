import React, { useState } from 'react';
import { StyleSheet, TextInput, Button, ScrollView, Image, ImageBackground, View, SafeAreaView } from 'react-native';
import { Text } from '@/components/Themed';

export default function TabTwoScreen() {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [emergencyContactName, setEmergencyContactName] = useState('');
  const [emergencyContactPhone, setEmergencyContactPhone] = useState('');
  const [medicalConditions, setMedicalConditions] = useState('');
  const [allergies, setAllergies] = useState('');
  const [medications, setMedications] = useState('');

  const handleSubmit = () => {
    const patientData = {
      name,
      age: isNaN(parseInt(age)) ? null : parseInt(age),
      gender,
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
    console.log(patientData);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={{ backgroundColor: 'white' }}>
        <Image
          source={require('./guardian_angels_bear.png')}
          style={styles.guardianAngel}
        />

        <Image
          source={require('./patient information form.png')}
          style={styles.patientInfoForm}
        />

        {renderInputField("Name", name, setName)}
        {renderInputField("Age", age, setAge, { keyboardType: "numeric" })}
        {renderInputField("Gender", gender, setGender)}
        {renderInputField("Emergency Contact Name", emergencyContactName, setEmergencyContactName)}
        {renderInputField("Emergency Contact Phone", emergencyContactPhone, setEmergencyContactPhone, { keyboardType: "phone-pad" })}
        {renderInputField("Medical Conditions (comma-separated)", medicalConditions, setMedicalConditions)}
        {renderInputField("Allergies (comma-separated, optional)", allergies, setAllergies)}
        {renderInputField("Medications (comma-separated, optional)", medications, setMedications)}

        <Button title="Submit" onPress={handleSubmit} />
      </ScrollView>
    </SafeAreaView>
  );
}

const renderInputField = (label, value, onChangeText, additionalProps = {}) => (
  <View style={styles.inputFieldContainer}>
    <Text style={styles.label}>{label}</Text>
    <ImageBackground
      source={require('./backgroundImage.png')}
      style={styles.inputBackground}
      imageStyle={styles.imageStyle}
    >
      <TextInput
        style={styles.input}
        placeholder={`Enter ${label.toLowerCase()}`}
        value={value}
        onChangeText={onChangeText}
        {...additionalProps}
      />
    </ImageBackground>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  guardianAngel: {
    width: 200,
    height: 200,
    alignSelf: 'center',
    resizeMode: 'contain',
    marginBottom: 10,
  },
  patientInfoForm: {
    width: 350,
    height: 350,
    alignSelf: 'center',
    resizeMode: 'contain',
    marginBottom: -150,
    marginTop: -170,
  },
  inputFieldContainer: {
    marginBottom: 15,
  },
  inputBackground: {
    width: '100%',
    height: 60,
    justifyContent: 'center',
    marginBottom: 10,
    borderRadius: 5,
    overflow: 'hidden',
    position: 'relative', // Set position to relative
  },
  label: {
    width: '100%',
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
    fontFamily: 'NewsReader',
    zIndex: 99,
    color: 'black',
  },
  input: {
    height: '100%',
    paddingHorizontal: 10,
    paddingVertical: 5,
    color: 'black',
    textAlign: 'center',
    fontSize: 16,
    fontFamily: 'NewsReader',
    position: 'absolute', // Set position to absolute
    zIndex: 99, // Ensure input is above the background
  },
  imageStyle: {
    borderRadius: 5,
  },
});

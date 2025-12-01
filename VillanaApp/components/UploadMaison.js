import React, { useState } from 'react';
import { Button, View, Image, TextInput } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

const UploadMaison = () => {
  const [images, setImages] = useState([]);
  const [formData, setFormData] = useState(new FormData());

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsMultipleSelection: true,
      quality: 1,
    });

    if (!result.cancelled) {
      const uri = result.uri;
      const name = uri.split('/').pop();
      const type = `image/${uri.split('.').pop()}`;

      formData.append('photos', { uri, name, type });
      setImages([...images, { uri }]);  // Garde une trace des images
    }
  };

  const handleUpload = () => {
    axios.post('http://10.125.36.64:8000/maisons/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      console.log('Upload successful', response.data);
    })
    .catch(error => {
      console.error('Upload failed', error);
    });
  };

  return (
    <View>
      <Button title="Select Images" onPress={pickImage} />
      {images.map((image, index) => (
        <Image key={index} source={{ uri: image.uri }} style={{ width: 100, height: 100 }} />
      ))}
      <Button title="Upload" onPress={handleUpload} />
    </View>
  );
};

export default UploadMaison;

import { CameraView,Camera } from 'expo-camera';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import React, { useEffect, useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import AppBar from './AppBar';

const CameraScreen = () => {
    const [hasPermission, setHasPermission] = useState(null);
    const [cameraType, setCameraType] = useState(Camera);
    const cameraRef = React.useRef(null);

    useEffect(() => {
        (async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            console.log('Camera permission status:', status);
            setHasPermission(status === 'granted');
        })();
    }, []);

    const takePicture = async () => {
        if (cameraRef.current) {
            const photo = await cameraRef.current.takePictureAsync();
            console.log(photo);
        }
    };

    const toggleFlash = () => {
       
       
    };

    const switchCamera = () => {
        setCameraType(
            cameraType === Camera.Constants.Type.back
                ? Camera.Constants.Type.front
                : Camera.Constants.Type.back
        );
    };

    const openGallery = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 1,
        });

        if (!result.cancelled) {
            console.log(result.uri);
        }
    };

    if (hasPermission === null) {
        return <View><Text>Requesting for camera permission</Text></View>;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }

    return (
        <View style={{ flex: 1 }}>
          
            <CameraView
                style={{ flex: 1 }}
                type={cameraType}
               
                ref={cameraRef}
            >
              <AppBar/>
                <View style={styles.TopContainer}>
                    <TouchableOpacity style={styles.button} onPress={toggleFlash}>
                        <Ionicons name= {'flash-off'} size={30} color="white" />
                    </TouchableOpacity>
                
                    <TouchableOpacity style={styles.button} onPress={switchCamera}>
                        <Ionicons name="camera-reverse" size={30} color="white" />
                    </TouchableOpacity>
                    
                </View>
                <View style={styles.buttongal}>
                    <TouchableOpacity style={styles.button} onPress={openGallery}>
                        <Ionicons name="images" size={35} color="white" />
                    </TouchableOpacity>
                </View>
                <View style={styles.buttoncam}>                   
                    <TouchableOpacity style={styles.button1} onPress={takePicture}>
                        <Ionicons name="camera" size={50} color="#444" />
                    </TouchableOpacity>                 
                </View>
            </CameraView>
        </View>
    );
};

const styles = StyleSheet.create({
    TopContainer: {
        position:'absolute',
        flexDirection: 'column',
        justifyContent: 'flex-end',
        alignItems: 'flex-end',
        padding: 20,
        left:0,
        right:0,
        marginTop:30,
        
    },
    buttongal: {
      position:'absolute',
      flexDirection: 'row',
      justifyContent: 'flex-start',
      alignItems: 'center',
      marginLeft:10,
      padding: 20,
      left:0,
      right:0,
      bottom:50
  },
  buttoncam: {
    position:'absolute',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    left:0,
    right:0,
    bottom:50

},
    button: {
        alignItems: 'center',
        backgroundColor: 'transparent',
        marginTop:20
    },
    button1: {
      alignItems: 'center',
      backgroundColor: 'white',
      height:70,
      width:70,
      borderRadius:50,
      alignItems:'center',
      justifyContent:'center'
  },
   
});

export default CameraScreen;
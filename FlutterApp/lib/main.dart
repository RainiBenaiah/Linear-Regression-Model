import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const IrrigationApp());
}

class IrrigationApp extends StatelessWidget {
  const IrrigationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Irrigation Prediction',
      theme: ThemeData(
        primarySwatch: Colors.green,
        useMaterial3: true,
      ),
      home: const PredictionScreen(),
    );
  }
}

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  State<PredictionScreen> createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;
  String? _predictionResult;
  final TextEditingController _temperatureController = TextEditingController();
  final TextEditingController _soilHumidityController = TextEditingController();
  final TextEditingController _timeController = TextEditingController();
  final TextEditingController _airTemperatureController = TextEditingController();
  final TextEditingController _windSpeedController = TextEditingController();
  final TextEditingController _airHumidityController = TextEditingController();
  final TextEditingController _windGustController = TextEditingController();
  final TextEditingController _pressureController = TextEditingController();

  Future<void> _submitForm() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
        _predictionResult = null;
      });

      try {
        // Add /predict to the endpoint URL
        final response = await http.post(
          Uri.parse('https://linear-regression-model-ihov.onrender.com/predict'),
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: json.encode({
            'temperature': double.parse(_temperatureController.text),
            'soil_humidity': double.parse(_soilHumidityController.text),
            'time': double.parse(_timeController.text),
            'air_temperature': double.parse(_airTemperatureController.text),
            'wind_speed': double.parse(_windSpeedController.text),
            'air_humidity': double.parse(_airHumidityController.text),
            'wind_gust': double.parse(_windGustController.text),
            'pressure': double.parse(_pressureController.text),
          }),
        );

        print('Response status code: ${response.statusCode}');
        print('Response body: ${response.body}');

        if (response.statusCode == 200) {
          final result = json.decode(response.body);
          setState(() {
            _predictionResult = 'Prediction: ${result['status']}';
          });
        } else {
          final errorBody = json.decode(response.body);
          throw Exception(
            'Server responded with status code ${response.statusCode}.'
                'Error: ${errorBody['detail'] ?? 'Unknown error'}',
          );

        }
      } catch (e) {
        print('Error details: $e');
        setState(() {
          if (e is FormatException) {
            _predictionResult = 'Error: Invalid response format from server';
          } else if (e is http.ClientException) {
            _predictionResult = 'Error: Could not connect to server. Please check your internet connection.';
          } else {
            _predictionResult = 'Error: ${e.toString()}';
          }
        });
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _testApiConnection() async {
    try {
      final response = await http.get(
        Uri.parse('https://linear-regression-model-ihov.onrender.com/health'),
      );
      print('Health check status code: ${response.statusCode}');
      print('Health check response: ${response.body}');
    } catch (e) {
      print('Health check error: $e');
    }
  }

  @override
  void initState() {
    super.initState();
    _testApiConnection();
  }

  Widget _buildNumberField({
    required String label,
    required TextEditingController controller,
    required double min,
    required double max,
    String? suffix,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(
          labelText: label,
          suffix: suffix != null ? Text(suffix) : null,
          border: const OutlineInputBorder(),
        ),
        validator: (value) {
          if (value == null || value.isEmpty) {
            return 'Please enter a value';
          }
          final number = double.tryParse(value);
          if (number == null) {
            return 'Please enter a valid number';
          }
          if (number < min || number > max) {
            return 'Please enter a value between $min and $max';
          }
          return null;
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Irrigation Prediction'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildNumberField(
                label: 'Temperature',
                controller: _temperatureController,
                min: -50,
                max: 50,
                suffix: '°C',
              ),
              _buildNumberField(
                label: 'Soil Humidity',
                controller: _soilHumidityController,
                min: 0,
                max: 100,
                suffix: '%',
              ),
              _buildNumberField(
                label: 'Time',
                controller: _timeController,
                min: 0,
                max: 24,
                suffix: 'hours',
              ),
              _buildNumberField(
                label: 'Air Temperature',
                controller: _airTemperatureController,
                min: -50,
                max: 50,
                suffix: '°C',
              ),
              _buildNumberField(
                label: 'Wind Speed',
                controller: _windSpeedController,
                min: 0,
                max: 150,
                suffix: 'Km/h',
              ),
              _buildNumberField(
                label: 'Air Humidity',
                controller: _airHumidityController,
                min: 0,
                max: 100,
                suffix: '%',
              ),
              _buildNumberField(
                label: 'Wind Gust',
                controller: _windGustController,
                min: 0,
                max: 200,
                suffix: 'Km/h',
              ),
              _buildNumberField(
                label: 'Pressure',
                controller: _pressureController,
                min: 80,
                max: 120,
                suffix: 'KPa',
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _isLoading ? null : _submitForm,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Predict'),
              ),
              if (_predictionResult != null)
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    _predictionResult!,
                    style: const TextStyle(fontSize: 18),
                    textAlign: TextAlign.center,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _temperatureController.dispose();
    _soilHumidityController.dispose();
    _timeController.dispose();
    _airTemperatureController.dispose();
    _windSpeedController.dispose();
    _airHumidityController.dispose();
    _windGustController.dispose();
    _pressureController.dispose();
    super.dispose();
  }
}
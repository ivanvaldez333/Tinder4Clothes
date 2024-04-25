import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        title: 'Namer App',
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyAppState extends ChangeNotifier {
  var current = WordPair.random();
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();

    return Scaffold(
      body: Column(
        children: [
          Container(
            margin: EdgeInsets.only(
                top: 90.0, left: 40.0, right: 40.0, bottom: 30.0),
            decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.grey,
                  width: 250,
                ),
                borderRadius: BorderRadius.circular(10.0)),
          ),
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            ElevatedButton(
              onPressed: () {
                print('button pressed!');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
                shape: CircleBorder(),
                fixedSize: Size.fromWidth(120),
                padding: EdgeInsets.all(35),
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
              child: Icon(Icons.clear_outlined, size: 24.0),
            ),
            ElevatedButton(
              onPressed: () {
                print('button pressed!');
              },
              style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  foregroundColor: Colors.white,
                  shape: CircleBorder(),
                  fixedSize: Size.fromWidth(120),
                  padding: EdgeInsets.all(35),
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
              child: Icon(Icons.star, size: 24.0),
            ),
            ElevatedButton(
                onPressed: () {
                  print('button pressed!');
                },
                style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                    foregroundColor: Colors.white,
                    shape: CircleBorder(),
                    fixedSize: Size.fromWidth(120),
                    padding: EdgeInsets.all(35),
                    tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                child: Icon(Icons.favorite, size: 24.0))
          ]),
        ],
      ),
    );
  }
}

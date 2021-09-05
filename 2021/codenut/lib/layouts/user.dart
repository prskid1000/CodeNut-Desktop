import 'package:CodeNut/components/frame.dart';
import 'package:CodeNut/store/store.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class User extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double width = MediaQuery.of(context).size.width;
    double height = MediaQuery.of(context).size.height;

    return Consumer<Store>(
      builder: (context, store, child) {
        return Frame(
          store.contribBuilder(context),
        );
      },
    );
  }
}

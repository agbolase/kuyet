import "package:flutter_test/flutter_test.dart";
import "package:tomato_care/main.dart";

void main() {
  testWidgets("TomatoCare boots", (tester) async {
    await tester.pumpWidget(const TomatoCareApp());
    await tester.pump();
    expect(find.textContaining("TomatoCare"), findsWidgets);
  });
}

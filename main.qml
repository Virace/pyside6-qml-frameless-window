import QtQuick
import QtQuick.Window
import QtQuick.Controls

//import io.qt.textproperties
Window {
    id: mainWindow
    width: 1200
    height: 720
    minimumWidth: 600
    minimumHeight: 400
    visible: true
    title: qsTr("Hello World")
    // 需要以下两缺一不可，没有Windows则会无法恢复窗口动画
    flags: Qt.FramelessWindowHint | Qt.Window

    // 透明, 配合亚克力或Aero
    color: "transparent"
    property int windowStatus: 0

    // 后端方法
    //    Function {
    //        id: func
    //    }
    // 自定义
    QtObject {
        id: internal
        function maximizeRestore() {
            if (windowStatus == 0) {
                mainWindow.showMaximized()
                windowStatus = 1
            } else {
                mainWindow.showNormal()
                windowStatus = 0
            }
        }

        function ifMaximizedWindowRestore() {
            if (windowStatus === 1) {
                mainWindow.showNormal()
                windowStatus = 0
            }
        }

        function restore() {
            windowStatus = 0
        }
    }
    Rectangle {
        id: titleBar
        height: 40
        color: "#6b1cd3"
        radius: 8
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 2
        anchors.leftMargin: 2
        anchors.topMargin: 2

        DragHandler {
            onActiveChanged: if (active) {
                                 mainWindow.startSystemMove()
                                 internal.ifMaximizedWindowRestore()
                             }
        }
        Button {
            id: btnClose
            x: 1140
            text: 'x'
            visible: true
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 8
            anchors.topMargin: 8
            onPressed: mainWindow.close()
        }
        Button {
            id: btnMaximizeRestore
            x: 1105
            text: '口'
            visible: true
            anchors.right: btnClose.left
            anchors.top: parent.top
            anchors.rightMargin: 0
            anchors.topMargin: 8
            onClicked: internal.maximizeRestore()
        }

        Button {
            id: btnMinimize
            x: 1070
            text: '-'
            visible: true
            anchors.right: btnMaximizeRestore.left
            anchors.top: parent.top
            anchors.rightMargin: 0
            anchors.topMargin: 8
            onClicked: {
                mainWindow.showMinimized()
                internal.restoreMargins()
            }
        }
    }
    Image {
        anchors.centerIn: parent
        source: 'src/tom.png'
        sourceSize.width: 200
        sourceSize.height: 200
    }

    onClosing: function (event) {
        console.log(event)
        //event.accepted = false
    }
}

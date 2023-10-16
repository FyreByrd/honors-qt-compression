#pragma once

struct Point { int x, y; };

template <typename E> class QuadNode
{
private:
    Point loc;      //location of the node in 2D space
    E data;         //value of the node
    Quadnode* tlc;  //top left child
    Quadnode* trc;  //top right child
    Quadnode* blc;  //bottom left child
    Quadnode* brc;  //bottom right child
public
    //default constructor
    QuadNode() { tlc = trc = blc = brc = NULL; }
    //constructor with data members
    QuadNode(Point p, E e, QuadNode tl = NULL, QuadNode tr = NULL, QuadNode bl = NULL, QuadNode br = NULL) {
        loc = p; data = e; tlc = tl; trc = tr; blc = bl; brc = br;
    }
    //destructor
    ~QuadNode() {}

    E& element() { return data; }
    void setElement(const E& e) { data = e; }
    Point& location() { return loc;  }
    void setLocation(const Point& p) { loc = p; }

    //<<<<<Getters and Setters for children>>>>>
    
    inline QuadNode* topLeft() const { return tlc; }
    void setTopLeft(QuadNode<E>* q) { tlc = q; }

    inline QuadNode* topRight() const { return trc; }
    void setTopRight(QuadNode<E>* q) { trc = q; }

    inline QuadNode* botLeft() const { return blc; }
    void setBotLeft(QuadNode<E>* q) { blc = q; }

    inline QuadNode* botRight() const { return brc; }
    void setBotRight(QuadNode<E>* q) { brc = q; }

    //return true if node is a leaf, false if otherwise
    bool isLeaf() { return tlc == NULL && trc == NULL && blc == NULL && brc == NULL; }
};
